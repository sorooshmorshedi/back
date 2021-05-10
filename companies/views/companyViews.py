from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from companies.models import Company
from companies.permissions import CompanyLimit
from companies.serializers import CompanySerializer
from helpers.auth import BasicCRUDPermission
from helpers.models import manage_files


class CompanyModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission, CompanyLimit)
    permission_basename = 'company'
    serializer_class = CompanySerializer

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        qs = Company.objects.hasAccess(self.request.method).filter(companyUsers__user=user)
        return qs.prefetch_related('financial_years')

    def perform_create(self, serializer: CompanySerializer) -> None:
        user = self.request.user
        serializer.save(
            superuser=user.get_superuser()
        )

    def perform_update(self, serializer: CompanySerializer) -> None:
        manage_files(serializer.instance, self.request.data, ['logo'])
        serializer.save()
