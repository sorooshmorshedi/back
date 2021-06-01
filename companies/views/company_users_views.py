from typing import Any, Type

from django.db.migrations.serializer import BaseSerializer
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from companies.models import CompanyUserInvitation, CompanyUser
from companies.serializers import CompanyUserInvitationSerializer, CompanyUserUpdateSerializer, \
    CompanyUserListRetrieveSerializer
from helpers.auth import BasicCRUDPermission
from helpers.sms import Sms
from server.settings import APP_SHORT_LINK
from users.models import User


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
        instance: CompanyUserInvitation = serializer.instance
        user = User.objects.filter(username=instance.username).first()
        if user:
            text = "شرکت {} شما را به نرم افزار حسابداری آنلاین سبحان دعوت نموده است.\nبرای تایید دعوت خود وارد پروفایل کاربری شوید\nآدرس: {}".format(
                self.company.name,
                APP_SHORT_LINK
            )
            Sms.send(user.phone, text)

    def perform_destroy(self, instance: CompanyUserInvitation) -> None:
        if instance.status != CompanyUserInvitation.PENDING:
            raise ValidationError(["وضعیت دعوت اجازه این عملیات را نمی دهد."])
        instance.delete()


class CompanyUserModelView(ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'user'
    serializer_class = CompanyUserInvitationSerializer

    def get_queryset(self) -> QuerySet:
        return CompanyUser.objects.hasAccess('get').filter(company=self.request.user.active_company)

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.request.method.lower() == 'put':
            return CompanyUserUpdateSerializer
        return CompanyUserListRetrieveSerializer
