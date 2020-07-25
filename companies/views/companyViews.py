from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from companies.models import Company
from companies.serializers import CompanySerializer
from helpers.auth import BasicCRUDPermission


class CompanyModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'company'
    queryset = Company.objects.prefetch_related('financial_years').all()
    serializer_class = CompanySerializer


