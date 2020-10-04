from rest_framework.viewsets import ModelViewSet

from sobhan_admin.serializers import AdminUserCreateSerializer, AdminUserUpdateSerializer
from users.models import User


class AdminUsersView(ModelViewSet):
    queryset = User.objects.filter(superuser=None).all()

    def get_serializer_class(self):
        if self.request.method.lower() == 'post':
            return AdminUserCreateSerializer
        return AdminUserUpdateSerializer

    def perform_create(self, serializer) -> None:
        serializer.save(
            superuser=None,
            is_superuser=True
        )
