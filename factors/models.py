from django.db import models
from django.db.models import signals
from django_jalali.db import models as jmodels

from accounts.accounts.models import Account, FloatAccount
from factors.signals import clearFactorSanad
from sanads.sanads.models import Sanad
from sanads.transactions.models import Transaction
from wares.models import Ware, Warehouse, updateInventory

EXPENSE_TYPES = (
    ('buy', 'خرید'),
    ('sale', 'فروش')
)

FACTOR_TYPES = (
    ('buy', 'خرید'),
    ('sale', 'فروش'),
    ('backFromBuy', 'بازگشت از خرید'),
    ('backFromSale', 'بازگشت از فروش'),

)

RAR_TYPES = (
    ('receipt', 'رسید'),
    ('remittance', 'حواله')
)

RECEIPT_CREATE_TYPES = (
    ('auto', 'auto'),
    ('manual', 'manual')
)


class Expense(models.Model):
    name = models.CharField(max_length=100, unique=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factorExpense')
    type = models.CharField(max_length=10, choices=EXPENSE_TYPES)
    explanation = models.CharField(max_length=255, blank=True)


class Receipt(models.Model):
    code = models.IntegerField()
    type = models.CharField(max_length=15, choices=RAR_TYPES)
    createType = models.CharField(max_length=20, choices=RECEIPT_CREATE_TYPES, default='manual')
    date = jmodels.jDateField()
    time = models.TimeField(blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.code, self.type)


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='items')
    ware = models.ForeignKey(Ware, on_delete=models.PROTECT, related_name='receiptItems')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='receiptItems')
    count = models.IntegerField()


class Factor(models.Model):
    code = models.IntegerField()
    sanad = models.ForeignKey(Sanad, on_delete=models.PROTECT, related_name='factor', blank=True, null=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.PROTECT, related_name='factor', blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factors')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factors', blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=15, choices=FACTOR_TYPES)
    paidValue = models.DecimalField(default=0, max_digits=24, decimal_places=0)

    date = jmodels.jDateField()
    time = models.TimeField(blank=True)

    created_at = jmodels.jDateField(auto_now=True)
    updated_at = jmodels.jDateField(auto_now_add=True)

    discountValue = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    discountPercent = models.IntegerField(default=0, null=True, blank=True)
    taxValue = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    taxPercent = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        unique_together = ('code', 'type')

    @property
    def sum(self):
        sum = 0
        for i in self.items.all():
            sum += i.fee * i.count
        return sum

    @property
    def discountSum(self):
        discountSum = 0
        if self.discountPercent:
            discountSum = self.discountPercent * self.sum / 100
        else:
            discountSum = self.discountValue
        for i in self.items.all():
            discountSum += i.discount
        return discountSum

    @property
    def taxSum(self):
        taxSum = 0
        if self.taxPercent:
            taxSum = self.taxPercent * (self.sum - self.discountSum) / 100
        else:
            taxSum = self.taxValue
        return taxSum


class FactorExpense(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.PROTECT, related_name='factorExpenses')
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='expenses')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='factorExpenses')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.PROTECT, related_name='factorExpenses', blank=True, null=True)
    value = models.DecimalField(max_digits=24, decimal_places=0)
    explanation = models.CharField(max_length=255, blank=True)


class FactorPayment(models.Model):
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='payments')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='payments')
    value = models.DecimalField(max_digits=24, decimal_places=0)

    class Meta:
        unique_together = ('factor', 'transaction')


class FactorItem(models.Model):
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='items')
    ware = models.ForeignKey(Ware, on_delete=models.PROTECT, related_name='factorItems')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='factorItems')

    count = models.IntegerField()
    fee = models.DecimalField(max_digits=24, decimal_places=0)
    discountValue = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True, blank=True)
    discountPercent = models.IntegerField(default=0, null=True, blank=True)

    @property
    def value(self):
        return self.fee * self.count

    @property
    def discount(self):
        if self.discountPercent:
            return self.value * self.discountPercent / 100
        else:
            return self.discountValue


def updateInventoryOnReceiptItemSave(sender, instance, raw, using, update_fields, **kwargs):
    if instance.id:
        oldCount = ReceiptItem.objects.get(pk=instance.id).count
    else:
        oldCount = 0
    count = instance.count - oldCount
    receipt = instance.receipt

    if receipt.type == 'remittance':
        count = -count
    updateInventory(instance.warehouse.id, instance.ware.id, count)


def updateInventoryOnReceiptItemDelete(sender, instance, using, **kwargs):
    updateInventory(instance.warehouse.id, instance.ware.id, -instance.count)


signals.post_delete.connect(receiver=clearFactorSanad, sender=Factor)
signals.pre_save.connect(receiver=updateInventoryOnReceiptItemSave, sender=ReceiptItem)
signals.pre_delete.connect(receiver=updateInventoryOnReceiptItemDelete, sender=ReceiptItem)


def clearReceipt(receipt):
    receipt.explanation = ''
    receipt.save()
    for item in receipt.items.all():
        item.delete()


def newReceiptCode():
    try:
        return Receipt.objects.latest('code').code + 1
    except:
        return 1
