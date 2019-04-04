from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer


class UserView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


@api_view(['post'])
def setActiveCompany(request):
    from companies.models import Company
    # TODO : check permissions
    user = request.user
    company = request.data.get('company', None)
    company = get_object_or_404(Company, pk=company)
    user.active_company = company
    user.active_financial_year = company.last_financial_year
    user.save()
    return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


@api_view(['post'])
def setActiveFinancialYear(request):
    from companies.models import FinancialYear
    # TODO : check permissions
    user = request.user
    financial_year = request.data.get('financial_year', None)
    financial_year = get_object_or_404(FinancialYear, pk=financial_year)
    user.active_company = financial_year.company
    user.active_financial_year = financial_year
    user.save()
    return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
