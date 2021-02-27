from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from distributions.models import CommissionRange, Visitor
from distributions.models.path import Path
from distributions.serializers.commission_range_serializers import CommissionRangeCreateUpdateSerializer, \
    CommissionRangeListRetrieveSerializer
from distributions.serializers.path_serializers import PathListRetrieveSerializer, PathCreateUpdateSerializer
from distributions.serializers.visitor_serializers import VisitorCreateUpdateSerializer, VisitorListRetrieveSerializer
from helpers.auth import BasicCRUDPermission
from helpers.functions import get_new_code, get_new_child_code


class CommissionRangeModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'commissionRange'
    serializer_class = CommissionRangeListRetrieveSerializer

    def get_queryset(self):
        return CommissionRange.objects.hasAccess(self.request.method, self.permission_basename)

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = CommissionRangeCreateUpdateSerializer(instance=self.get_object(), data=data['item'])
        serializer.is_valid(raise_exception=True)

        instance = serializer.instance
        instance.sync(data['items'])

        return Response(CommissionRangeListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = CommissionRangeCreateUpdateSerializer(data=data['item'])
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=request.user.active_financial_year
        )

        instance = serializer.instance
        instance.sync(data['items'])

        return Response(CommissionRangeListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)


class VisitorModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'visitor'
    serializer_class = VisitorListRetrieveSerializer

    def get_queryset(self):
        return Visitor.objects.hasAccess(self.request.method, self.permission_basename)

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = VisitorCreateUpdateSerializer(instance=self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance

        return Response(VisitorListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = VisitorCreateUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        level = data['level']
        if level == 0:
            code = Visitor.get_new_code()
        else:
            parent = get_object_or_404(Visitor, pk=data.get('parent'))
            code = parent.get_new_child_code()

        serializer.save(
            financial_year=request.user.active_financial_year,
            code=code
        )

        return Response(
            VisitorListRetrieveSerializer(instance=serializer.instance).data,
            status=status.HTTP_200_OK
        )


class PathModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'path'
    serializer_class = PathListRetrieveSerializer

    def get_queryset(self):
        return Path.objects.hasAccess(self.request.method, self.permission_basename)

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = PathCreateUpdateSerializer(
            instance=self.get_object(),
            data=data,
            context={"visitors": data.get('visitors', [])}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance

        return Response(PathListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = PathCreateUpdateSerializer(
            data=data,
            context={"visitors": data.get('visitors', [])}
        )
        serializer.is_valid(raise_exception=True)

        level = data['level']
        if level == 0:
            code = Path.get_new_code()
        else:
            parent = get_object_or_404(Path, pk=data.get('parent'))
            code = parent.get_new_child_code()

        serializer.save(
            financial_year=request.user.active_financial_year,
            code=code
        )

        instance = serializer.instance

        return Response(
            PathListRetrieveSerializer(instance=instance).data,
            status=status.HTTP_200_OK
        )
