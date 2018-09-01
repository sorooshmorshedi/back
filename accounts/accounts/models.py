from django.db import models

from accounts.costCenters.models import CostCenter, CostCenterGroup

ACCOUNT_LEVELS = (
    (0, 'group'),
    (1, 'kol'),
    (2, 'moein'),
    (3, 'tafzili'),
)


class FloatAccountGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return str(self.pk) + ' - ' + self.name


class FloatAccount(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    max_bed = models.CharField(max_length=20, blank=True, null=True)
    max_bes = models.CharField(max_length=20, blank=True, null=True)
    max_bed_with_sanad = models.CharField(max_length=20, blank=True, null=True)
    max_bes_with_sanad = models.CharField(max_length=20, blank=True, null=True)
    is_disabled = models.BooleanField(default=False)

    floatAccountGroup = models.ForeignKey(FloatAccountGroup, on_delete=models.PROTECT, related_name='floatAccounts')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()


class AccountType(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=3, choices=(('BED', 'bedehkar'),('BES', 'bestankar')))

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.name


class IndependentAccount(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
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

    permissions = (
        ('get_account', 'Can get accounts')
    )

    def __str__(self):
        return "{0} - {1}".format(self.code, self.name)

    class Meta:
        ordering = ['code', ]


class Person(models.Model):

    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='person', primary_key=True)

    phone1 = models.CharField(max_length=20, null=True, blank=True)
    phone2 = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
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


class Bank(models.Model):

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
