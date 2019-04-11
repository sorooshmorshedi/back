from django.db import models
from django.db.models import Sum
from accounts.costCenters.models import CostCenterGroup
from helpers.models import BaseModel


class FloatAccountGroup(BaseModel):

    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'گروه حساب شناور'

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.name)


class FloatAccount(BaseModel):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    max_bed = models.CharField(max_length=20, blank=True, null=True)
    max_bes = models.CharField(max_length=20, blank=True, null=True)
    max_bed_with_sanad = models.CharField(max_length=20, blank=True, null=True)
    max_bes_with_sanad = models.CharField(max_length=20, blank=True, null=True)
    is_disabled = models.BooleanField(default=False)

    floatAccountGroups = models.ManyToManyField(FloatAccountGroup, through='FloatAccountRelation',
                                                related_name='floatAccounts')

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        verbose_name = 'حساب شناور'


class FloatAccountRelation(BaseModel):
    floatAccountGroup = models.ForeignKey(FloatAccount, on_delete=models.CASCADE, related_name='relation')
    floatAccount = models.ForeignKey(FloatAccountGroup, on_delete=models.CASCADE, related_name='relation')


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
    programingName = models.CharField(max_length=255, unique=True, blank=True, null=True)
    nature = models.CharField(max_length=3, choices=(('bed', 'بدهکار'), ('bes', 'بستانکار'), ('non', 'خنثی')))
    usage = models.CharField(max_length=30, choices=ACCOUNT_TYPE_USAGES, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'نوع حساب'

    def __str__(self):
        return "{} - {} - {} - {}".format(self.name, self.nature, self.usage, self.programingName)


class IndependentAccount(BaseModel):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'حساب مستقل'

    def __str__(self):
        return self.name


class Account(BaseModel):

    GROUP = 0
    KOL = 1
    MOEIN = 2
    TAFSILI = 3
    ACCOUNT_LEVELS = (
        (GROUP, 'group'),
        (KOL, 'kol'),
        (MOEIN, 'moein'),
        (TAFSILI, 'tafzili'),
    )

    name = models.CharField(max_length=150, verbose_name='نام حساب')
    code = models.CharField(max_length=50, verbose_name='کد حساب')
    explanation = models.CharField(max_length=255, blank=True, null=True)
    is_disabled = models.BooleanField(default=False)

    max_bed = models.IntegerField(blank=True, null=True)
    max_bes = models.IntegerField( blank=True, null=True)
    max_bed_with_sanad = models.IntegerField(blank=True, null=True)
    max_bes_with_sanad = models.IntegerField(blank=True, null=True)

    created_at = models.DateField(auto_now=True, null=True)
    updated_at = models.DateField(auto_now_add=True, null=True)

    level = models.IntegerField(choices=ACCOUNT_LEVELS)

    type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, related_name='accounts', blank=True, null=True)
    costCenterGroup = models.ForeignKey(CostCenterGroup, on_delete=models.PROTECT, related_name='accounts', blank=True, null=True)
    floatAccountGroup = models.ForeignKey(FloatAccountGroup, on_delete=models.PROTECT, related_name='accounts', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)

    def __str__(self):
        return "{0} - {1}".format(self.code, self.name)

    class Meta(BaseModel.Meta):
        ordering = ['code', ]
        verbose_name = 'حساب'
        verbose_name_plural = 'حساب ها'
        permissions = (
            ('create_account', 'تعریف حساب'),
            ('retrieve_account', 'مشاهده حساب'),
            ('update_account', 'ویرایش حساب'),
            ('delete_account', 'حذف حساب'),
        )

    def can_delete(self):
        return self.level != 0 and self.sanadItems.count() == 0

    def get_remain(self):
        from sanads.sanads.models import SanadItem
        bed = SanadItem.objects.filter(account__code__startswith=self.code, valueType='bed') \
            .aggregate(Sum('value'))['value__sum']
        bes = SanadItem.objects.filter(account__code__startswith=self.code, valueType='bes') \
            .aggregate(Sum('value'))['value__sum']

        if not bed:
            bed = 0
        if not bes:
            bes = 0

        remain_type = '-'
        remain = bed - bes
        if remain > 0:
            remain_type = 'bed'
        elif remain < 0:
            remain = -remain
            remain_type = 'bes'

        remain = {
            'value': remain,
            'remain_type': remain_type
        }

        return remain

    @staticmethod
    def get_inventory_account(user):
        return Account.objects.inFinancialYear(user).get(code='106040001')

    @staticmethod
    def get_partners_account(user):
        return Account.objects.inFinancialYear(user).get(code='303070001')


class Person(BaseModel):


    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='person', primary_key=True)

    personType = models.CharField(choices=(('real', 'حقیقی'), ('legal', 'حقوقی')), max_length=5)

    phone1 = models.CharField(max_length=20, null=True, blank=True)
    phone2 = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    meli_code = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    postalCode = models.CharField(max_length=20, null=True, blank=True)
    accountNumber1 = models.CharField(max_length=50, null=True, blank=True)
    accountNumber2 = models.CharField(max_length=50, null=True, blank=True)
    eghtesadiCode = models.CharField(max_length=50, null=True, blank=True)

    type = models.CharField(choices=(('buyer', 'buyer'), ('seller', 'seller')), max_length=10)

    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.account.code, self.account.name)

    class Meta(BaseModel.Meta):
        verbose_name = 'حساب اشخاص'
        verbose_name_plural = 'حساب های اشخاص'
        permissions = (
            ('create_buyer', 'تعریف حساب خریدار'),
            ('retrieve_buyer', 'مشاهده حساب خریدار'),
            ('update_buyer', 'ویرایش حساب خریدار'),
            ('delete_buyer', 'حذف حساب خریدار'),
        )


class Bank(BaseModel):


    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='bank', primary_key=True)

    name = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    branchCode = models.CharField(max_length=20, null=True, blank=True)
    accountNumber = models.CharField(max_length=50, null=True, blank=True)
    sheba = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)

    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.account.code, self.account.name)

    class Meta(BaseModel.Meta):
        verbose_name = 'حساب بانک'
