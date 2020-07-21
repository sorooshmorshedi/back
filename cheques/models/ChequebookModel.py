from django.db import models
from rest_framework.exceptions import ValidationError

from accounts.accounts.models import Account, FloatAccount
from companies.models import FinancialYear
from helpers.models import BaseModel


class Chequebook(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='chequebooks')

    code = models.IntegerField()
    serial = models.CharField(max_length=255, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='chequebook')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='chequebook', blank=True,
                                     null=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='chequebooksAsCostCenter',
                                   blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)
    serial_from = models.IntegerField()
    serial_to = models.IntegerField()

    def __str__(self):
        return "{0} - {1}".format(self.account.title, self.serial, )

    class Meta(BaseModel.Meta):
        verbose_name = 'دفتر چک'
        permission_basename = 'chequebook'
        permissions = (
            ('get.chequebook', 'مشاهده دفتر چک'),
            ('create.chequebook', 'تعریف دفتر چک'),
            ('update.chequebook', 'ویرایش دفتر چک'),
            ('delete.chequebook', 'حذف دفتر چک'),

            ('getOwn.chequebook', 'مشاهده دفتر چک های خود'),
            ('updateOwn.chequebook', 'ویرایش دفتر چک های خود'),
            ('deleteOwn.chequebook', 'حذف دفتر چک های خود'),
        )

    def save(self, *args, **kwargs):

        created = not self.id
        res = super(Chequebook, self).save(*args, **kwargs)

        if created:
            self._create_cheques()
        else:
            for cheque in self.cheques.all():
                cheque.delete()
            self._create_cheques()

        return res

    def _create_cheques(self):
        from cheques.models.ChequeModel import Cheque
        for i in range(self.serial_from, self.serial_to + 1):
            self.cheques.create(
                serial=i,
                status='blank',
                received_or_paid=Cheque.PAID,
                account=self.account,
                floatAccount=self.floatAccount,
                costCenter=self.costCenter,
                bankName=self.account.name,
                branchName=self.account.branch_name,
                accountNumber=self.account.account_number,
                financial_year=self.financial_year
            )

    def is_deletable(self, raise_exception=False):
        for cheque in self.cheques.all():
            if cheque.status != 'blank':
                raise ValidationError("برای ویرایش یا حذف دسته چک، باید وضعیت همه چک های آن سفید باشد")

    @staticmethod
    def newCode(user):
        try:
            last_chequebook = Chequebook.objects.inFinancialYear().latest('code')
            code = last_chequebook.code + 1
        except:
            code = 1

        return code
