from typing import Any

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from sobhan_admin.permissions import IsStaff
from sobhan_admin.serializers import AdminUserListRetrieveSerializer, AdminProfileSerializer
from users.models import User
from users.serializers import UserCreateSerializer, UserUpdateSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class AdminLoginView(APIView):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_staff:
            raise ValidationError("شما اجازه دسترسی به این صفحه را ندارید")
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class AdminUsersView(ModelViewSet):
    permission_classes = (IsAuthenticated, IsStaff,)
    queryset = User.objects.filter(superuser=None).all()
    serializer_class = AdminUserListRetrieveSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data
        profile_data = data.pop('profile')

        serializer = UserCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            superuser=None,
            is_superuser=True
        )

        profile_serializer = AdminProfileSerializer(data=profile_data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save(
            user=serializer.instance
        )

        return Response(AdminUserListRetrieveSerializer(serializer.instance).data)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = self.get_object()
        data = request.data
        profile_data = data.pop('profile')

        serializer = UserUpdateSerializer(user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        profile_serializer = AdminProfileSerializer(serializer.instance.profile, data=profile_data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        return Response(AdminUserListRetrieveSerializer(serializer.instance).data)
