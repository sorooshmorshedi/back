from django.db.models import QuerySet
from django.db.models.query_utils import Q
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from helpers.auth import BasicCRUDPermission
from users.models import User, PhoneVerification
from users.permissions import DeleteUserPermission, ChangePasswordPermission
from users.serializers import UserListRetrieveSerializer, UserCreateSerializer, UserUpdateSerializer


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
            Q(superuser=self.request.user.get_superuser()) | Q(id=self.request.user.id)
        )


class UserCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'user'
    serializer_class = UserCreateSerializer

    def get_queryset(self) -> QuerySet:
        return User.objects.hasAccess('post')

    def perform_create(self, serializer: UserCreateSerializer) -> None:
        user = self.request.user
        serializer.save(
            superuser=user.get_superuser()
        )


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'user'
    serializer_class = UserUpdateSerializer

    def get_queryset(self) -> QuerySet:
        return User.objects.hasAccess('put').filter(
            Q(superuser=self.request.user.get_superuser()) | Q(id=self.request.user.id)
        )


class UserDestroyView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission, DeleteUserPermission)
    permission_basename = 'user'
    serializer_class = UserUpdateSerializer

    def get_queryset(self) -> QuerySet:
        return User.objects.hasAccess('delete').filter(
            Q(superuser=self.request.user.get_superuser()) | Q(id=self.request.user.id)
        )


class UserChangePasswordView(APIView):
    permission_classes = (IsAuthenticated, ChangePasswordPermission)

    def post(self, request):
        user = get_object_or_404(
            User.objects.hasAccess('get', 'user').filter(
                Q(superuser=self.request.user.get_superuser()) | Q(id=self.request.user.id)
            ),
            pk=request.data.get('user')
        )
        request.user.has_object_perm(user, 'changePassword', raise_exception=True)
        user.set_password(request.data.get('password'))
        user.save()
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


class SendVerificationCodeForForgetPasswordView(APIView):
    throttle_scope = 'verification_code'

    def post(self, request):
        PhoneVerification.send_verification_code(request.data.get('phone'), has_user=True)
        return Response({})


class ChangePasswordByVerificationCodeView(APIView):
    # throttle_scope = 'verification_code'

    def post(self, request):
        data = request.data
        phone = data.get('phone')
        code = data.get('code')
        new_password = data.get('new_password')
        phone_verification = PhoneVerification.check_verification(phone, code, raise_exception=True)

        user = phone_verification.user
        user.set_password(new_password)
        user.save()
        return Response({})
