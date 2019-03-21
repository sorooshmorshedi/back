from django.db import models

from accounts.costCenters.models import CostCenter, CostCenterGroup
from helpers.models import BaseModel

ACCOUNT_LEVELS = (
    (0, 'group'),
    (1, 'kol'),
    (2, 'moein'),
    (3, 'tafzili'),
)

ACCOUNT_TYPE_USAGES = (
    ('incomeStatement', 'سود و زیان'),
    ('balanceSheet', 'ترازنامه'),
    ('none', 'هیچ کدام')
)


class FloatAccountGroup(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'گروه حساب شناور'

    def __str__(self):
        return str(self.pk) + ' - ' + self.name


class FloatAccount(BaseModel):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    max_bed = models.CharField(max_length=20, blank=True, null=True)
    max_bes = models.CharField(max_length=20, blank=True, null=True)
    max_bed_with_sanad = models.CharField(max_length=20, blank=True, null=True)
    max_bes_with_sanad = models.CharField(max_length=20, blank=True, null=True)
    is_disabled = models.BooleanField(default=False)

    floatAccountGroups = models.ManyToManyField(FloatAccountGroup, related_name='floatAccounts')

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        verbose_name = 'حساب شناور'


class AccountType(BaseModel):
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
    name = models.CharField(max_length=150, verbose_name='نام حساب')
    code = models.CharField(max_length=50, unique=True, verbose_name='کد حساب')
    explanation = models.CharField(max_length=255, blank=True, null=True)
    is_disabled = models.BooleanField(default=False)

    bed = models.DecimalField(max_digits=24, decimal_places=0, default=0)
    bes = models.DecimalField(max_digits=24, decimal_places=0, default=0)

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
        return self.sanadItems.count() == 0


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
