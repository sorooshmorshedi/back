from django.db import models

from companies.models import FinancialYear
from helpers.models import BaseModel


class ReportsPermissions(models.Model):
    class Meta:
        default_permissions = ()

        """
            Reports permissions codenames should end with `Report` 
        """

        permissions = (
            ('get.accountBalanceReport', 'مشاهده تراز'),
            ('get.floatAccountBalanceByGroupReport', 'مشاهده تراز شناور بر اساس گروه'),
            ('get.floatAccountBalanceReport', 'مشاهده تراز شناور'),

            ('get.balanceSheetReport', 'مشاهده ترازنامه'),
            ('get.incomeStatementReport', 'مشاهده گزارش سود و زیان تفصیلی'),

            ('get.buyReport', 'مشاهده گزارش خرید'),
            ('get.saleReport', 'مشاهده گزارش فروش'),

            ('get.wareInventoryReport', 'مشاهده کاردکس کالا'),
            ('get.allWaresInventoryReport', 'مشاهده کاردکس همه کالا ها'),
            ('get.warehouseInventoryReport', 'مشاهده کاردکس انبار'),
            ('get.allWarehousesInventoryReport', 'مشاهده کاردکس همه انبار ها'),

            ('get.sanadItemsReport', 'مشاهده گزارشات ردیف اسناد (دفتر روزنامه، صورت حساب تفصیلی و دفاتر حساب ها)'),

            ('get.accountsCodingReport', 'مشاهده گزارش کدینگ حساب ها'),
        )


class ExportVerifier(BaseModel):
    SANAD = 's'

    FACTOR_BUY = 'fb'
    FACTOR_SALE = 'fs'
    FACTOR_BACK_FROM_BUY = 'fbfb'
    FACTOR_BACK_FROM_SALE = 'fbfs'
    FACTOR_RECEIPT = 'frc'
    FACTOR_REMITTANCE = 'frm'
    CONSUMPTION_WARE_REMITTANCE = 'cwr'
    FIRST_PERIOD_INVENTORY = 'fpi'

    PRE_FACTOR_BUY = 'pfb'
    PRE_FACTOR_SALE = 'pfs'

    TRANSACTION_RECEIVE = 'tr'
    TRANSACTION_PAYMENT = 'tp'

    TRANSFER = 't'

    INPUT_ADJUSTMENT = 'ia'
    OUTPUT_ADJUSTMENT = 'oa'

    FORMS = (
        (SANAD, 'سند'),
        (FACTOR_BUY, 'فاکتور خرید'),
        (FACTOR_SALE, 'فاکتور فروش'),
        (FACTOR_BACK_FROM_BUY, 'فاکتور برگشت از خرید'),
        (FACTOR_BACK_FROM_SALE, 'فاکتور برگشت از فروش'),
        (TRANSACTION_RECEIVE, 'دریافت'),
        (TRANSACTION_PAYMENT, 'پرداخت'),
        (TRANSFER, 'انتقال'),
        (CONSUMPTION_WARE_REMITTANCE, 'حواله کالای مصرفی'),
        (FIRST_PERIOD_INVENTORY, 'موجودی اول دوره'),
        (INPUT_ADJUSTMENT, 'رسید تعدیل انبار'),
        (OUTPUT_ADJUSTMENT, 'حواله تعدیل انبار'),
        (PRE_FACTOR_BUY, 'پیش فاکتور خرید'),
        (PRE_FACTOR_SALE, 'پیش فاکتور فروش'),
        (FACTOR_RECEIPT, 'رسید'),
        (FACTOR_REMITTANCE, 'حواله')
    )

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='export_verifiers')
    name = models.CharField(max_length=200, blank=True, null=True)
    post = models.CharField(max_length=255)
    form = models.CharField(choices=FORMS, max_length=4)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permissions = (
            ('create.exportVerifier', 'تعریف تایید کنندگان خروجی'),

            ('get.exportVerifier', 'مشاهده تایید کنندگان خروجی'),
            ('update.exportVerifier', 'ویرایش تایید کنندگان خروجی'),
            ('delete.exportVerifier', 'حذف تایید کنندگان خروجی'),

            ('getOwn.exportVerifier', 'مشاهده تایید کنندگان خروجی خود'),
            ('updateOwn.exportVerifier', 'ویرایش تایید کنندگان خروجی خود'),
            ('deleteOwn.exportVerifier', 'حذف تایید کنندگان خروجی خود'),
        )

    def __str__(self):
        form_name = ''
        for form in self.FORMS:
            if self.form == form[0]:
                form_name = form[1]
                break
        return "{} {} ({})".format(self.name, self.post, form_name)
