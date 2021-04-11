from django.db import models

from companies.models import FinancialYear
from helpers.models import BaseModel


class Option(BaseModel):
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=255, unique=True)
    usage = models.CharField(max_length=100, blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    class Meta(BaseModel.Meta):
        permission_basename = 'option'
        permissions = (
            ('get.option', 'مشاهده تنظیمات'),
            ('update.option', 'ویرایش تنظیمات'),
        )

    @staticmethod
    def get_option(codename):
        codename = str(codename)
        try:
            option = Option.objects.get(codename=codename)
        except Option.DoesNotExist:
            option = Option.objects.create(codename=codename)
        return option

    @staticmethod
    def get_value(codename, default=None):
        value = Option.get_option(codename).value
        return value if value else default

    @staticmethod
    def set_value(codename, value):
        option = Option.get_option(codename)
        option.value = str(value)
        option.save()

    @staticmethod
    def get_order_id():
        last_order_id = Option.get_value('order_id')
        last_order_id = int(last_order_id) if last_order_id else 0
        last_order_id += 1
        Option.set_value('order_id', last_order_id)
        return last_order_id


class DefaultText(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)

    usage = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    value = models.TextField(blank=True, null=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permission_basename = 'defaultText'
        permissions = (
            ('get.defaultText', 'مشاهده متن های پیشفرض'),
            ('update.defaultText', 'ویرایش متن های پیشفرض'),
        )

    @staticmethod
    def get(key, financial_year=None):
        qs = DefaultText.objects.inFinancialYear(financial_year)
        text = qs.filter(key=key).first()
        return text.value
