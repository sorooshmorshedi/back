from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.permissions import ChangePasswordPermission
from users.serializers import UserListRetrieveSerializer, UserCreateSerializer, UserUpdateSerializer


class CurrentUserApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(UserListRetrieveSerializer(request.user).data, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserListRetrieveSerializer


class UserCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDestroyView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserChangePasswordView(APIView):
    permission_classes = (IsAuthenticated, ChangePasswordPermission)

    def post(self, request):
        user = get_object_or_404(User, pk=request.data.get('user'))
        user.set_password(request.data.get('password'))
        user.save()
        return Response([])


class SetActiveCompany(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        from companies.models import Company
        # TODO : check permissions
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
        # TODO : check permissions
        user = request.user
        financial_year = request.data.get('financial_year', None)
        financial_year = get_object_or_404(FinancialYear, pk=financial_year)
        user.active_company = financial_year.company
        user.active_financial_year = financial_year
        user.save()
        return Response(UserListRetrieveSerializer(user).data, status=status.HTTP_200_OK)
