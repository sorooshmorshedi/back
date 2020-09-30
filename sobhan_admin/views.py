from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from sobhan_admin.serializers import AdminUserSerializer
from users.models import User


class AdminUsersView(ModelViewSet):
    serializer_class = AdminUserSerializer
    queryset = User.objects.filter(superuser=None).all()

    def perform_create(self, serializer: AdminUserSerializer) -> None:
        serializer.save(
            superuser=None,
            is_superuser=True
        )
        # instance = serializer.instance
        # instance.is_superuser = True
        # instance.save()
