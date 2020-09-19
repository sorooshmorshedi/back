from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from companies.models import Company
from companies.serializers import CompanySerializer
from helpers.auth import BasicCRUDPermission


class CompanyModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'company'
    serializer_class = CompanySerializer

    def get_queryset(self) -> QuerySet:
        return Company.objects.hasAccess(self.request.method).prefetch_related('financial_years').filter(
            superuser=self.request.user.get_superuser()
        )

    def perform_create(self, serializer: CompanySerializer) -> None:
        user = self.request.user
        serializer.save(
            superuser=user.get_superuser()
        )
