from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from companies.models import Company, FinancialYear
from rest_framework import generics

from companies.permissions import CompanyListCreate, CompanyDetail
from companies.serializers import CompanySerializer, FinancialYearSerializer


@method_decorator(csrf_exempt, name='dispatch')
class CompanyModelView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, CompanyListCreate,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class FinancialYearModelView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    queryset = FinancialYear.objects.all()
    serializer_class = FinancialYearSerializer
