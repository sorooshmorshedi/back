from django.db.models import QuerySet
from django.db.models.query_utils import Q
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from companies.models import CompanyUserInvitation, CompanyUser
from helpers.auth import BasicCRUDPermission
from users.models import User, PhoneVerification
from users.permissions import ChangePasswordPermission
from users.serializers import UserListRetrieveSerializer, UserCreateSerializer, UserUpdateSerializer, \
    UserInvitationsListSerializer


class CurrentUserApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(UserListRetrieveSerializer(request.user).data, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'user'
    serializer_class = UserListRetrieveSerializer

    def get_queryset(self) -> QuerySet:
        return User.objects.hasAccess('get').filter(
            companyUsers__company=self.request.user.active_company
        )


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def get_queryset(self) -> QuerySet:
        return User.objects.all()


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'user'
    serializer_class = UserUpdateSerializer

    def get_queryset(self) -> QuerySet:
        return User.objects.all()


class UserChangePasswordView(APIView):
    permission_classes = (IsAuthenticated, ChangePasswordPermission)

    def post(self, request):
        user = request.user

        qs = User.objects.hasAccess('get', 'user')
        if not user.is_staff:
            qs.filter(
                Q(superuser=user.get_superuser()) | Q(id=user.id)
            )

        user = get_object_or_404(qs, pk=request.data.get('user'))
        request.user.has_object_perm(user, 'changePassword', raise_exception=True)
        user.set_password(request.data.get('password'))
        user.save()

        if hasattr(user, 'auth_token'):
            token = user.auth_token
            if token:
                token.delete()

        return Response([])


class SetActiveCompany(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        from companies.models import Company
        user = request.user
        company = request.data.get('company', None)
        company = get_object_or_404(Company, pk=company)
        user.active_company = company
        user.active_financial_year = company.last_financial_year
        user.save()
        return Response(UserListRetrieveSerializer(user).data, status=status.HTTP_200_OK)


class SetActiveFinancialYear(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        from companies.models import FinancialYear
        user = request.user
        financial_year = request.data.get('financial_year', None)
        financial_year = get_object_or_404(FinancialYear, pk=financial_year)
        user.active_company = financial_year.company
        user.active_financial_year = financial_year
        user.save()
        return Response(UserListRetrieveSerializer(user).data, status=status.HTTP_200_OK)


class SendVerificationCodeView(APIView):
    throttle_scope = 'verification_code'

    def post(self, request):
        PhoneVerification.send_verification_code(request.data.get('phone'))
        return Response({})


class ChangePasswordByVerificationCodeView(APIView):
    throttle_scope = 'verification_code'

    def post(self, request):
        data = request.data
        phone = data.get('phone')
        username = data.get('username')
        code = data.get('code')
        new_password = data.get('new_password')
        PhoneVerification.check_verification(phone, code, raise_exception=True)

        try:
            user = get_object_or_404(User, username=username, phone=phone)
        except User.DoesNotExist:
            raise ValidationError('نام کاربری اشتباه می باشد')

        user.set_password(new_password)
        user.save()
        return Response({})


class UserInvitationsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInvitationsListSerializer

    def get_queryset(self) -> QuerySet:
        return CompanyUserInvitation.objects.filter(username=self.request.user.username)


class ChangeUserInvitationStatusView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        invitation = get_object_or_404(CompanyUserInvitation, pk=data.get('id'))
        new_status = data.get('status')

        if invitation.status == invitation.PENDING:
            if new_status == invitation.ACCEPTED:
                confirmation_code = data.get('confirmation_code')
                if confirmation_code != invitation.confirmation_code:
                    return Response(
                        ['کد تایید اشتباه می باشد.'],
                        status=status.HTTP_400_BAD_REQUEST
                    )

                company_user, created = CompanyUser.objects.get_or_create(
                    user=request.user,
                    company=invitation.company,
                )
                company_user.financialYears.set(invitation.financialYears.all())
                company_user.roles.set(invitation.roles.all())

            invitation.status = new_status
            invitation.save()

            return Response([], status.HTTP_200_OK)
        else:
            return Response(['دعوت غیر قابل ویرایش می باشد.'], status=status.HTTP_400_BAD_REQUEST)
