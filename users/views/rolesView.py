from django.contrib.auth.models import Permission
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer
from users.models import Role
from users.serializers import RoleSerializer, PermissionListSerializer


class PermissionListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Permission.objects.all()
    serializer_class = PermissionListSerializer


class RoleListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(
            company=self.request.user.active_company,
        )


class RoleUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleDestroyView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
