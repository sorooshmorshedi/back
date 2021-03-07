from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from distributions.models.distribution_model import Distribution
from distributions.reports.filters import DistributionFilter
from distributions.serializers.distribution_serializers import DistributionListSerializer
from helpers.auth import BasicCRUDPermission
from reports.lists.export_views import BaseListExportView


class DistributionListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_basename = 'distribution'

    serializer_class = DistributionListSerializer
    filterset_class = DistributionFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Distribution.objects.hasAccess('get', self.permission_basename).all()


class DistributionListExportView(DistributionListView, BaseListExportView):
    filename = 'distribution'
    title = "لیست تحویل ها"

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)
