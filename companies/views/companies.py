from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from companies.models import Company, FinancialYear
from companies.serializers import CompanySerializer, FinancialYearSerializer


@method_decorator(csrf_exempt, name='dispatch')
class CompanyModelView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, CompanyListCreate,)
    queryset = Company.objects.prefetch_related('financial_years').all()
    serializer_class = CompanySerializer


class FinancialYearModelView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    queryset = FinancialYear.objects.all()
    serializer_class = FinancialYearSerializer
