from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from companies.models import CompanyUserInvitation
from companies.serializers import CompanyUserInvitationSerializer
from helpers.auth import BasicCRUDPermission


class CompanyUserInvitationModelView(ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'user'
    serializer_class = CompanyUserInvitationSerializer

    @property
    def company(self):
        return self.request.user.active_company

    def get_queryset(self) -> QuerySet:
        return CompanyUserInvitation.objects.hasAccess('get').filter(company=self.company)

    def perform_create(self, serializer: CompanyUserInvitationSerializer) -> None:
        serializer.save(
            company=self.company
        )

    def perform_destroy(self, instance: CompanyUserInvitation) -> None:
        if instance.status != CompanyUserInvitation.PENDING:
            raise ValidationError(["وضعیت دعوت اجازه این عملیات را نمی دهد."])
        instance.delete()
