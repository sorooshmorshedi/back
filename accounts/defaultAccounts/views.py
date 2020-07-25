from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.defaultAccounts.serializers import *
from helpers.auth import BasicCRUDPermission
from helpers.views.RetrieveUpdateDestroyAPIViewWithAutoFinancialYear import \
    RetrieveUpdateDestroyAPIViewWithAutoFinancialYear
from helpers.views.ListCreateAPIViewWithAutoFinancialYear import ListCreateAPIViewWithAutoFinancialYear


@method_decorator(csrf_exempt, name='dispatch')
class DefaultAccountListCreate(ListCreateAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'defaultAccount'
    serializer_class = DefaultAccountSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = DefaultAccountListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)


class DefaultAccountDetail(RetrieveUpdateDestroyAPIViewWithAutoFinancialYear):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'defaultAccount'
    serializer_class = DefaultAccountSerializer

    def retrieve(self, request, **kwargs):
        da = self.get_object()
        serializer = DefaultAccountListRetrieveSerializer(da)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        da = self.get_object()
        if da.codename:
            raise serializers.ValidationError('این پیشفرض غیر قابل حذف می باشد')
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs) -> Response:
        return super().update(request, *args, **kwargs)
