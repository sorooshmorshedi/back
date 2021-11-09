from typing import Type

from django.db.models import QuerySet
from django.db.models.expressions import Exists, OuterRef
from django.db.models.query import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView

from _dashtbashi.filters import LadingBillSeriesFilter, RemittanceFilter, LadingFilter, LadingBillNumberFilter, \
    OtherDriverPaymentFilter
from _dashtbashi.models import Driver, Car, Driving, Association, Remittance, Lading, LadingBillSeries, \
    LadingBillNumber, OilCompanyLading, OtherDriverPayment, OilCompanyLadingItem
from _dashtbashi.serializers import DriverSerializer, CarSerializer, DrivingCreateUpdateSerializer, \
    DrivingListRetrieveSerializer, AssociationSerializer, RemittanceListRetrieveSerializer, \
    RemittanceCreateUpdateSerializer, LadingListSerializer, LadingCreateUpdateSerializer, \
    LadingBillSeriesSerializer, OilCompanyLadingCreateUpdateSerializer, OilCompanyLadingItemCreateUpdateSerializer, \
    OilCompanyLadingListRetrieveSerializer, OtherDriverPaymentListRetrieveSerializer, \
    OtherDriverPaymentCreateUpdateSerializer, LadingBillNumberListSerializer, LadingRetrieveSerializer
from helpers.auth import BasicCRUDPermission
from helpers.functions import get_object_by_code, get_new_code
from helpers.views.MassRelatedCUD import MassRelatedCUD
from helpers.views.confirm_view import ConfirmView
from imprests.models import ImprestSettlement, ImprestSettlementItem
from transactions.models import Transaction
from transactions.serializers import TransactionCreateUpdateSerializer
from transactions.transaction_sanad import TransactionSanad


class DriverModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'driver'
    serializer_class = DriverSerializer

    def get_queryset(self) -> QuerySet:
        return Driver.objects.hasAccess(self.request.method)

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(
            financial_year=self.request.user.active_financial_year
        )


class CarModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'car'
    serializer_class = CarSerializer

    def get_queryset(self) -> QuerySet:
        return Car.objects.hasAccess(self.request.method)

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(
            financial_year=self.request.user.active_financial_year
        )


class DrivingModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'driving'

    def get_queryset(self) -> QuerySet:
        return Driving.objects.hasAccess(self.request.method)

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.request.method.lower() == 'get':
            return DrivingListRetrieveSerializer
        return DrivingCreateUpdateSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(
            financial_year=self.request.user.active_financial_year
        )


class AssociationModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'association'
    serializer_class = AssociationSerializer

    def get_queryset(self) -> QuerySet:
        return Association.objects.hasAccess(self.request.method)

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(
            financial_year=self.request.user.active_financial_year
        )


class LadingBillSeriesModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'ladingBillSeries'
    serializer_class = LadingBillSeriesSerializer
    filterset_class = LadingBillSeriesFilter
    pagination_class = LimitOffsetPagination
    page_size = 15

    def get_queryset(self) -> QuerySet:
        return LadingBillSeries.objects.hasAccess(self.request.method).prefetch_related(
            Prefetch(
                'numbers',
                LadingBillNumber.objects.annotate(
                    is_free=~Exists(Lading.objects.filter(billNumber=OuterRef('pk')))
                ).filter(is_free=True, is_revoked=False, lading=None)
            )
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def is_editable(self):
        instance = self.get_object()
        if Lading.objects.filter(billNumber__series=instance).exists():
            raise ValidationError("قبل از ویرایش سری بارنامه بارگیری های آن را حذف کنید")

    def update(self, *args, **kwargs):
        self.is_editable()
        return super().update(*args, **kwargs)

    def destroy(self, *args, **kwargs):
        self.is_editable()
        return super().destroy(*args, **kwargs)


class LadingBillSeriesByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'ladingBillSeries'

    def get(self, request):
        item = get_object_by_code(
            LadingBillSeries.objects.hasAccess(request.method),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if item:
            return Response(LadingBillSeriesSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


class RemittanceModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'remittance'
    filterset_class = RemittanceFilter
    pagination_class = LimitOffsetPagination
    page_size = 15

    def get_queryset(self) -> QuerySet:
        return Remittance.objects.hasAccess(self.request.method)

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.request.method.lower() == 'get':
            return RemittanceListRetrieveSerializer
        return RemittanceCreateUpdateSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(
            financial_year=self.request.user.active_financial_year,
        )


class RemittanceByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'remittance'

    def get(self, request):
        remittance = get_object_by_code(
            Remittance.objects.hasAccess(request.method),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if remittance:
            return Response(RemittanceListRetrieveSerializer(instance=remittance).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


class RemittanceByCodeView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'remittance'

    def get(self, request):
        remittance = get_object_or_404(Remittance.objects.hasAccess(request.method), code=request.GET.get('code'))
        return Response(RemittanceListRetrieveSerializer(instance=remittance).data)


class LadingModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'lading'
    filterset_class = LadingFilter

    def get_queryset(self) -> QuerySet:
        return Lading.objects.hasAccess(self.request.method)

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.request.method.lower() == 'get':
            if 'pk' in self.kwargs:
                return LadingRetrieveSerializer
            else:
                return LadingListSerializer

        return LadingCreateUpdateSerializer

    def create(self, request, *args, **kwargs) -> Response:
        data = request.data.copy()
        data['financial_year'] = self.request.user.active_financial_year.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            LadingListSerializer(instance=serializer.instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class LadingByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'lading'

    def get(self, request):
        lading = get_object_by_code(
            Lading.objects.hasAccess(request.method),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if lading:
            return Response(LadingRetrieveSerializer(instance=lading).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


class RevokeLadingBillNumberView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_codename = 'revoke.ladingBillNumber'

    def post(self, request, *args, **kwargs):
        ladingBillNumber = get_object_or_404(
            LadingBillNumber.objects.hasAccess(request.method),
            pk=request.data.get('id')
        )
        request.user.has_object_perm(ladingBillNumber, self.permission_codename, raise_exception=True)

        ladingBillNumber.is_revoked = request.data.get('is_revoked')
        ladingBillNumber.revoked_at = request.data.get('date')
        ladingBillNumber.save()

        return Response()


class LadingBillNumberListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_codename = 'get.ladingBillSeries'
    serializer_class = LadingBillNumberListSerializer

    ordering_fields = '__all__'
    filterset_class = LadingBillNumberFilter
    pagination_class = LimitOffsetPagination

    def get_queryset(self) -> QuerySet:
        only_not_used = self.request.GET.copy().get('not_used', False) == 'true'
        qs = LadingBillNumber.objects.all()
        if only_not_used:
            qs = qs.annotate(
                has_lading=Exists(Lading.objects.filter(billNumber=OuterRef('pk')))
            ).filter(has_lading=False)
        return qs


class OilCompanyLadingModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'oilCompanyLading'
    serializer_class = OilCompanyLadingCreateUpdateSerializer

    def get_queryset(self) -> QuerySet:
        return OilCompanyLading.objects.hasAccess(self.request.method)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        serialized = OilCompanyLadingListRetrieveSerializer(instance)
        return Response(serialized.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        form_data = data['form']
        items_data = data['items']

        serializer = OilCompanyLadingCreateUpdateSerializer(data=form_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=user.active_financial_year,
        )

        instance = serializer.instance
        MassRelatedCUD(
            user,
            items_data.get('items'),
            items_data.get('ids_to_delete'),
            'oilCompanyLading',
            serializer.instance.id,
            OilCompanyLadingItemCreateUpdateSerializer,
            OilCompanyLadingItemCreateUpdateSerializer,
        ).sync()

        return Response(OilCompanyLadingListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        user = request.user
        form_data = request.data['form']
        items_data = request.data['items']

        serialized = self.serializer_class(instance=instance, data=form_data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        MassRelatedCUD(
            user,
            items_data.get('items'),
            items_data.get('ids_to_delete'),
            'oilCompanyLading',
            instance.id,
            OilCompanyLadingItemCreateUpdateSerializer,
            OilCompanyLadingItemCreateUpdateSerializer,
        ).sync()

        return Response(OilCompanyLadingListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)


class OilCompanyLadingByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'oilCompanyLading'

    def get(self, request):
        item = get_object_by_code(
            OilCompanyLading.objects.hasAccess(request.method),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if item:
            return Response(OilCompanyLadingListRetrieveSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


class OtherDriverPaymentModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'otherDriverPayment'
    serializer_class = OtherDriverPaymentListRetrieveSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = OtherDriverPaymentFilter
    ordering_fields = '__all__'

    def get_queryset(self) -> QuerySet:
        return OtherDriverPayment.objects.hasAccess(self.request.method)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        item_data = data['item']
        payment_data = data['payment']

        payment_data['date'] = item_data['date']
        payment_data['type'] = Transaction.PAYMENT

        serializer = TransactionCreateUpdateSerializer(data=payment_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=user.active_financial_year,
            code=Transaction.newCodes(Transaction.PAYMENT),
            is_auto_created=True,
        )
        payment = serializer.instance
        payment.sync(user, payment_data)

        serializer = OtherDriverPaymentCreateUpdateSerializer(data=item_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=user.active_financial_year,
            payment=payment,
            code=get_new_code(OtherDriverPayment)
        )
        instance: OtherDriverPayment = serializer.instance
        car = instance.driving.car
        driver = instance.driving.driver

        for lading in instance.ladings.all():
            lading.is_paid = True
            lading.save()

        for imprest in instance.imprests.all():
            explanation = "تسویه شده توسط پرداخت رانندگان متفرقه"
            ImprestSettlement.settle_imprest(
                imprest,
                instance.date,
                account=car.payableAccount,
                floatAccount=driver.floatAccount,
                explanation=explanation,
            )

        TransactionSanad(payment).update()

        return Response(OtherDriverPaymentListRetrieveSerializer(instance=instance).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance: OtherDriverPayment = self.get_object()

        for lading in instance.ladings.all():
            lading.is_paid = False
            lading.save()

        for imprest in instance.imprests.all():
            imprest_settlement = getattr(imprest, 'imprestSettlement', None)
            if imprest_settlement and imprest_settlement.is_auto_created:
                imprest_settlement.delete()
            else:
                ImprestSettlementItem.objects.filter(
                    imprestSettlement=imprest_settlement,
                    is_auto_created=True,
                ).delete()

        payment = instance.payment

        instance.delete()

        payment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class OtherDriverPaymentByPositionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'otherDriverPayment'

    def get(self, request):
        item = get_object_by_code(
            OtherDriverPayment.objects.hasAccess(request.method),
            request.GET.get('position'),
            request.GET.get('id')
        )
        if item:
            return Response(OtherDriverPaymentListRetrieveSerializer(instance=item).data)
        return Response(['not found'], status=status.HTTP_404_NOT_FOUND)


class SettleDriverImprests(APIView):
    permission_basename = 'otherDriverPayment'

    def post(self, request):
        data = request.data
        car = Car.objects.get(pk=data['car'])
        driver = Driver.objects.get(pk=data['driver'])
        imprests = Transaction.objects.filter(
            is_defined=True,
            type=Transaction.IMPREST,
            pk__in=data['imprests']
        )

        settlements = []
        for imprest in imprests:
            explanation = "تسویه شده توسط پرداخت رانندگان متفرقه"
            settlement = ImprestSettlement.settle_imprest(
                imprest,
                data['date'],
                account=car.payableAccount,
                floatAccount=driver.floatAccount,
                explanation=explanation,
            )
            settlements.append(settlement.id)

        return Response(settlements)


class ConfirmRemittance(ConfirmView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'remittance'
    model = Remittance


class ConfirmLading(ConfirmView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'lading'
    model = Lading


class ConfirmOilCompanyLading(ConfirmView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'oilCompanyLading'
    model = OilCompanyLading


class ConfirmOtherDriverPayment(ConfirmView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'otherDriverPayment'
    model = OtherDriverPayment
