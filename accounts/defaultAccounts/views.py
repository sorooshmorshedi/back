from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.defaultAccounts.serializers import *
from helpers.auth import BasicCRUDPermission


@method_decorator(csrf_exempt, name='dispatch')
class DefaultAccountListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = DefaultAccountSerializer

    def get_queryset(self):
        return DefaultAccount.objects.inFinancialYear(self.request.user)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = DefaultAccountListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)


class DefaultAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = DefaultAccountSerializer

    def get_queryset(self):
        return DefaultAccount.objects.inFinancialYear(self.request.user)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        da = get_object_or_404(queryset, pk=pk)
        serializer = DefaultAccountListRetrieveSerializer(da)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        queryset = self.get_queryset()
        da = get_object_or_404(queryset, pk=pk)
        if da.programingName:
            raise serializers.ValidationError('این پیشفرض غیر قابل حذف می باشد')
        return super(DefaultAccountDetail, self).delete(request, pk)



