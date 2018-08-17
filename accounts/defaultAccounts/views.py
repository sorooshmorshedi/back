from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from accounts.defaultAccounts.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class DefaultAccountListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    queryset = DefaultAccount.objects.all()
    serializer_class = DefaultAccountSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = DefaultAccount.objects.all()
        serializer = DefaultAccountListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)


class DefaultAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, RPTypeDetail,)
    queryset = DefaultAccount.objects.all()
    serializer_class = DefaultAccountSerializer

    def retrieve(self, request, pk=None):
        queryset = DefaultAccount.objects.all()
        da = get_object_or_404(queryset, pk=pk)
        serializer = DefaultAccountListRetrieveSerializer(da)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        queryset = DefaultAccount.objects.all()
        da = get_object_or_404(queryset, pk=pk)
        if da.programingName:
            raise serializers.ValidationError('این پیشفرض غیر قابل حذف می باشد')
        return super(DefaultAccountDetail, self).delete(request, pk)



