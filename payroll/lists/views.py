from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from helpers.auth import BasicCRUDPermission
from payroll.lists.filters import WorkshopFilter, PersonnelFilter, PersonnelFamilyFilter, WorkshopPersonnelFilter, \
    ContractRowFilter, LeaveOrAbsenceFilter
from payroll.models import Workshop, Personnel, PersonnelFamily, WorkshopPersonnel, ContractRow, Contract
from payroll.serializers import WorkShopSerializer, PersonnelSerializer, PersonnelFamilySerializer, \
    WorkshopPersonnelSerializer, ContractRowSerializer, LeaveOrAbsenceSerializer


class WorkshopListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.workshop"
    serializer_class = WorkShopSerializer
    filterset_class = WorkshopFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Workshop.objects.hasAccess('get', self.permission_codename).all()


class PersonnelListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.personnel"
    serializer_class = PersonnelSerializer
    filterset_class = PersonnelFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Personnel.objects.hasAccess('get', self.permission_codename).all()


class PersonnelFamilyListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.personnel_family"
    serializer_class = PersonnelFamilySerializer
    filterset_class = PersonnelFamilyFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return PersonnelFamily.objects.hasAccess('get', self.permission_codename).all()


class ContractListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.contract"
    serializer_class = Contract
    filterset_class = Contract
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Contract.objects.hasAccess('get', self.permission_codename).all()


class WorkshopPersonnelListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.workshop_personnel"
    serializer_class = WorkshopPersonnel
    filterset_class = WorkshopPersonnel
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return WorkshopPersonnel.objects.hasAccess('get', self.permission_codename).all()


class ContractRowListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.contract_row"
    serializer_class = ContractRowSerializer
    filterset_class = ContractRowFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return ContractRow.objects.hasAccess('get', self.permission_codename).all()


class LeaveOrAbsenceListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.leave_or_absence"
    serializer_class = LeaveOrAbsenceSerializer
    filterset_class = LeaveOrAbsenceFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return ContractRow.objects.hasAccess('get', self.permission_codename).all()
