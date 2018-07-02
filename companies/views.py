from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated

from companies.models import Company
from rest_framework import generics

from companies.permissions import CompanyListCreate, CompanyDetail
from companies.serializers import CompanySerializer


@method_decorator(csrf_exempt, name='dispatch')
class CompanyListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, CompanyListCreate,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, CompanyDetail,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
