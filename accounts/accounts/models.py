from builtins import tuple
from typing import Union

from django.db import models
from django.db.models import Sum
from django.db.models.aggregates import Max
from django.db.models.functions.comparison import Coalesce

from companies.models import FinancialYear
from helpers.functions import get_new_child_code
from helpers.models import BaseModel, PHONE, MELLI_CODE, POSTAL_CODE, DECIMAL
from wares.models import SalePriceType


class FloatAccountGroup(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='floatAccountGroups')
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    is_cost_center = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permission_basename = 'floatAccountGroup'
        permissions = (
            ('get.floatAccountGroup', 'مشاهده گروه های حساب شناور / مرکز هزینه و درآمد'),
            ('create.floatAccountGroup', 'تعریف گروه حساب شناور / مرکز هزینه و درآمد'),
            ('update.floatAccountGroup', 'ویرایش گروه حساب شناور / مرکز هزینه و درآمد'),
            ('delete.floatAccountGroup', 'حذف گروه حساب شناور / مرکز هزینه و درآمد'),

            ('getOwn.floatAccountGroup', 'مشاهده گروه های حساب شناور / مرکز هزینه و درآمد خود'),
            ('updateOwn.floatAccountGroup', 'ویرایش گروه حساب شناور / مرکز هزینه و درآمد خود'),
            ('deleteOwn.floatAccountGroup', 'حذف گروه حساب شناور / مرکز هزینه و درآمد خود'),
        )

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.name)


class FloatAccount(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='floatAccounts')
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    is_cost_center = models.BooleanField(default=False)

    max_bed = DECIMAL(blank=True, null=True)
    max_bes = DECIMAL(blank=True, null=True)
    max_bed_with_sanad = DECIMAL(blank=True, null=True)
    max_bes_with_sanad = DECIMAL(blank=True, null=True)
    is_disabled = models.BooleanField(default=False)

    floatAccountGroups = models.ManyToManyField(FloatAccountGroup, through='FloatAccountRelation',
                                                related_name='floatAccounts')

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permission_basename = 'floatAccount'
        permissions = (
            ('get.floatAccount', 'مشاهده حساب های شناور'),
            ('create.floatAccount', 'تعریف حساب شناور'),
            ('update.floatAccount', 'ویرایش حساب شناور'),
            ('delete.floatAccount', 'حذف حساب شناور'),

            ('getOwn.floatAccount', 'مشاهده حساب های شناور خود'),
            ('updateOwn.floatAccount', 'ویرایش حساب شناور خود'),
            ('deleteOwn.floatAccount', 'حذف حساب شناور خود'),
        )


class FloatAccountRelation(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='floatAccountRelations')
    floatAccountGroup = models.ForeignKey(FloatAccountGroup, on_delete=models.CASCADE, related_name='relation')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.CASCADE, related_name='relation')

    class Meta(BaseModel.Meta):
        backward_financial_year = True


class AccountType(BaseModel):
    INCOME_STATEMENT = 'incomeStatement'
    BALANCE_SHEET = 'balanceSheet'
    NONE = 'none'

    ACCOUNT_TYPE_USAGES = (
        (INCOME_STATEMENT, 'سود و زیان'),
        (BALANCE_SHEET, 'ترازنامه'),
        (NONE, 'هیچ کدام')
    )

    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=255, unique=True, blank=True, null=True)
    nature = models.CharField(max_length=3, choices=(('bed', 'بدهکار'), ('bes', 'بستانکار'), ('non', 'خنثی')))
    usage = models.CharField(max_length=30, choices=ACCOUNT_TYPE_USAGES, blank=True)

    class Meta(BaseModel.Meta):
        backward_financial_year = True

    def __str__(self):
        return "{} - {} - {} - {}".format(self.name, self.nature, self.usage, self.codename)


class Account(BaseModel):
    GROUP = 0
    KOL = 1
    MOEIN = 2
    TAFSILI = 3
    ACCOUNT_LEVELS = (
        (GROUP, 'group'),
        (KOL, 'kol'),
        (MOEIN, 'moein'),
        (TAFSILI, 'tafsili'),
    )

    PERSON = 'p'
    BANK = 'b'
    OTHER = 'o'
    ACCOUNT_TYPES = (
        (PERSON, 'اشخاص'),
        (BANK, 'بانک'),
        (OTHER, 'دیگر')
    )

    BUYER = 'b'
    SELLER = 's'
    BUYER_OR_SELLER_CHOICES = (
        (BUYER, 'خریدار'),
        (SELLER, 'فروشنده'),
    )

    REAL = 'r'
    LEGAL = 'l'
    CONTRACTOR = 'c'
    PERSON_TYPES = (
        (REAL, 'حقیقی'),
        (LEGAL, 'حقوقی'),
        (CONTRACTOR, 'پیمانکاران'),
        (OTHER, 'دیگر')
    )

    CODE_LENGTHS = [1, 2, 2, 4]

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='accounts')
    account_type = models.CharField(max_length=2, choices=ACCOUNT_TYPES, default=OTHER)

    name = models.CharField(max_length=150, verbose_name='نام حساب')
    code = models.CharField(max_length=50, verbose_name='کد حساب')
    explanation = models.CharField(max_length=255, blank=True, null=True)
    is_disabled = models.BooleanField(default=False)

    max_bed = DECIMAL(blank=True, null=True)
    max_bes = DECIMAL(blank=True, null=True)
    max_bed_with_sanad = models.IntegerField(blank=True, null=True)
    max_bes_with_sanad = models.IntegerField(blank=True, null=True)

    created_at = models.DateField(auto_now=True, null=True)
    updated_at = models.DateField(auto_now_add=True, null=True)

    level = models.IntegerField(choices=ACCOUNT_LEVELS)

    type = models.ForeignKey(AccountType, on_delete=models.PROTECT, related_name='accounts')
    costCenterGroup = models.ForeignKey(FloatAccountGroup, on_delete=models.PROTECT,
                                        related_name='accountsAsCostCenter', blank=True, null=True)
    floatAccountGroup = models.ForeignKey(FloatAccountGroup, on_delete=models.PROTECT, related_name='accounts',
                                          blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)

    # Person fields
    person_type = models.CharField(choices=PERSON_TYPES, max_length=10, default="", blank=True)
    buyer_or_seller = models.CharField(choices=BUYER_OR_SELLER_CHOICES, max_length=10, default="", blank=True)
    defaultSalePriceType = models.ForeignKey(SalePriceType, on_delete=models.PROTECT, null=True)

    path = models.ForeignKey('distributions.Path', on_delete=models.PROTECT, related_name='accounts', blank=True,
                             null=True)

    phone_1 = models.CharField(max_length=20, default="", blank=True)
    phone_2 = models.CharField(max_length=20, default="", blank=True)
    mobile = PHONE(null=True, blank=True)
    melli_code = MELLI_CODE(null=True, blank=True)
    website = models.URLField(default="", blank=True)
    fax = models.CharField(max_length=20, default="", blank=True)
    email = models.EmailField(default="", blank=True)
    address_1 = models.CharField(max_length=255, default="", blank=True)
    address_2 = models.CharField(max_length=255, default="", blank=True)
    city = models.CharField(max_length=255, default="", blank=True)
    province = models.CharField(max_length=255, default="", blank=True)
    postal_code = POSTAL_CODE(null=True, blank=True)
    account_number_1 = models.CharField(max_length=50, default="", blank=True)
    account_number_2 = models.CharField(max_length=50, default="", blank=True)
    eghtesadi_code = models.CharField(max_length=50, default="", blank=True)

    # Bank Fields
    branch_name = models.CharField(max_length=100, default="", blank=True)
    branch_code = models.CharField(max_length=20, default="", blank=True)
    account_number = models.CharField(max_length=50, default="", blank=True)
    sheba = models.CharField(max_length=50, default="", blank=True)
    phone = models.CharField(max_length=30, default="", blank=True)

    def __str__(self):
        return self.title

    class Meta(BaseModel.Meta):
        ordering = ['code']
        backward_financial_year = True

        permissions = (
            ('get.account', 'مشاهده حساب ها'),

            ('create.account0', 'تعریف گروه'),
            ('update.account0', 'ویرایش گروه'),
            ('delete.account0', 'حذف گروه'),

            ('create.account1', 'تعریف کل'),
            ('update.account1', 'ویرایش کل'),
            ('delete.account1', 'حذف کل'),

            ('create.account2', 'تعریف معین'),
            ('update.account2', 'ویرایش معین'),
            ('delete.account2', 'حذف معین'),

            ('create.account3', 'تعریف تفصیلی'),
            ('update.account3', 'ویرایش تفصیلی'),
            ('delete.account3', 'حذف تفصیلی'),

            ('getOwn.account', 'مشاهده حساب ها خود'),

            ('updateOwn.account0', 'ویرایش گروه خود'),
            ('deleteOwn.account0', 'حذف گروه خود'),

            ('updateOwn.account1', 'ویرایش کل خود'),
            ('deleteOwn.account1', 'حذف کل خود'),

            ('updateOwn.account2', 'ویرایش معین خود'),
            ('deleteOwn.account2', 'حذف معین خود'),

            ('updateOwn.account3', 'ویرایش تفصیلی خود'),
            ('deleteOwn.account3', 'حذف تفصیلی خود'),
        )

    @property
    def title(self):
        return "{0} - {1}".format(self.code, self.name)

    def has_turnover(self):
        from sanads.models import SanadItem
        return SanadItem.objects.inFinancialYear().filter(account=self).exists()

    def can_delete(self):
        return self.level != 0 and self.sanadItems.count() == 0

    def get_new_child_code(self):

        if self.level == self.TAFSILI:
            return None

        last_child_code = None
        last_child = self.children.order_by('-code').first()
        if last_child:
            last_child_code = last_child.code

        return get_new_child_code(
            self.code,
            self.CODE_LENGTHS[self.level + 1],
            last_child_code
        )

    @staticmethod
    def get_new_group_code():
        code = Account.objects.filter(level=Account.GROUP).aggregate(Max('code'))['code__max']
        code = int(code) + 1

        if code >= 10:
            from rest_framework import serializers
            raise serializers.ValidationError("تعداد حساب های این سطح پر شده است")

        return str(code)

    @staticmethod
    def get_inventory_account(user):
        return Account.objects.inFinancialYear().get(code='106040001')

    @staticmethod
    def get_cost_of_sold_wares_account(user):
        return Account.objects.inFinancialYear().get(code='701010001')

    def get_balance(self):
        bed = bes = 0
        balances = AccountBalance.objects.inFinancialYear().filter(account__code__startswith=self.code).all()
        for balance in balances:
            bed += balance.bed
            bes += balance.bes
        remain = abs(bed - bes)
        return {
            'bed': bed,
            'bes': bes,
            'remain': remain
        }


class AccountBalance(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='accountsBalance')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='balance')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.CASCADE, related_name='balance', blank=True,
                                     null=True)
    costCenter = models.ForeignKey(FloatAccount, on_delete=models.CASCADE, related_name='balanceAsCostCenter',
                                   blank=True,
                                   null=True)

    bed = models.DecimalField(max_digits=24, decimal_places=0, default=0)
    bes = models.DecimalField(max_digits=24, decimal_places=0, default=0)

    class Meta(BaseModel.Meta):
        pass

    def __str__(self):
        return "{}, Bed: {}, Bes: {}".format(self.account, self.bed, self.bes)

    @staticmethod
    def update_balance(financial_year, account, bed_change=0, bes_change=0, floatAccount=None, costCenter=None):
        account_balance, created = AccountBalance.objects.get_or_create(
            financial_year=financial_year,
            account=account,
            floatAccount=floatAccount,
            costCenter=costCenter,
        )
        account_balance.bed += bed_change
        account_balance.bes += bes_change
        if account_balance.bed == account_balance.bes == 0:
            account_balance.delete()
        else:
            account_balance.save()

    @staticmethod
    def get_bed_bes(account=None, floatAccount=None, costCenter=None, financial_year=None) -> tuple:
        qs = AccountBalance.objects.inFinancialYear(financial_year)

        if account:
            qs = qs.filter(account=account)

        if floatAccount:
            qs = qs.filter(floatAccount=floatAccount)

        if costCenter:
            qs = qs.filter(costCenter=costCenter)

        result = qs.aggregate(
            bed_sum=Coalesce(Sum('bed'), 0),
            bes_sum=Coalesce(Sum('bes'), 0),
        )

        return result['bed_sum'], result['bes_sum']

    @staticmethod
    def get_balance(account, floatAccount=None, costCenter=None):
        bed, bes = AccountBalance.get_bed_bes(account, floatAccount, costCenter)
        balance = bed - bes
        return balance


class AccountGroup:
    def __init__(
            self,
            account: Union[Account, int, str],
            float_account: Union[FloatAccount, int, str] = None,
            cost_center: Union[FloatAccount, int, str] = None
    ):
        if account:
            if not isinstance(account, Account):
                account = Account.objects.get(pk=account)

        if float_account:
            if isinstance(float_account, FloatAccount):
                assert float_account.is_cost_center == False
            else:
                float_account: FloatAccount = FloatAccount.objects.get(is_cost_center=False, pk=float_account)
                assert account.floatAccountGroup in float_account.floatAccountGroups.all()

        if cost_center:
            if isinstance(cost_center, FloatAccount):
                assert cost_center.is_cost_center == True
            else:
                cost_center: FloatAccount = FloatAccount.objects.get(is_cost_center=True, pk=cost_center)
                assert account.floatAccountGroup in cost_center.floatAccountGroups.all()

        self.account = account
        self.floatAccount = float_account
        self.costCenter = cost_center

    @property
    def account_id(self):
        return self.account.id if self.account else None

    @property
    def floatAccount_id(self):
        return self.floatAccount.id if self.floatAccount else None

    @property
    def costCenter_id(self):
        return self.costCenter.id if self.costCenter else None
