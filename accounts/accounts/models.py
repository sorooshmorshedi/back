from django.db import models
from django.db.models import Sum
from django.db.models.aggregates import Max

from helpers.models import BaseModel


class FloatAccountGroup(BaseModel):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    is_cost_center = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        pass

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.name)


class FloatAccount(BaseModel):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    is_cost_center = models.BooleanField(default=False)

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
        pass


class FloatAccountRelation(BaseModel):
    floatAccountGroup = models.ForeignKey(FloatAccountGroup, on_delete=models.CASCADE, related_name='relation')
    floatAccount = models.ForeignKey(FloatAccount, on_delete=models.CASCADE, related_name='relation')


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

    BUYER_PERSON = 'b'
    SELLER_PERSON = 's'
    PERSON_TYPES = (
        (BUYER_PERSON, 'خریدار'),
        (SELLER_PERSON, 'فروشنده'),
    )

    CODE_LENGTHS = [1, 3, 5, 9]
    PARENT_PART = [0, 1, 3, 5]

    account_type = models.CharField(max_length=2, choices=ACCOUNT_TYPES, default=OTHER)

    name = models.CharField(max_length=150, verbose_name='نام حساب')
    code = models.CharField(max_length=50, verbose_name='کد حساب')
    explanation = models.CharField(max_length=255, blank=True, null=True)
    is_disabled = models.BooleanField(default=False)

    max_bed = models.IntegerField(blank=True, null=True)
    max_bes = models.IntegerField(blank=True, null=True)
    max_bed_with_sanad = models.IntegerField(blank=True, null=True)
    max_bes_with_sanad = models.IntegerField(blank=True, null=True)

    created_at = models.DateField(auto_now=True, null=True)
    updated_at = models.DateField(auto_now_add=True, null=True)

    level = models.IntegerField(choices=ACCOUNT_LEVELS)

    type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, related_name='accounts', blank=True, null=True)
    costCenterGroup = models.ForeignKey(FloatAccountGroup, on_delete=models.PROTECT,
                                        related_name='accountsAsCostCenter', blank=True, null=True)
    floatAccountGroup = models.ForeignKey(FloatAccountGroup, on_delete=models.PROTECT, related_name='accounts',
                                          blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)

    bed = models.DecimalField(max_digits=24, decimal_places=0, default=0)
    bes = models.DecimalField(max_digits=24, decimal_places=0, default=0)

    # Person fields
    is_real = models.BooleanField(default=True)
    person_type = models.CharField(choices=PERSON_TYPES, max_length=10, default="", blank="true")
    phone_1 = models.CharField(max_length=20, default="", blank=True)
    phone_2 = models.CharField(max_length=20, default="", blank=True)
    mobile = models.CharField(max_length=20, default="", blank=True)
    melli_code = models.CharField(max_length=20, default="", blank=True)
    website = models.URLField(default="", blank=True)
    fax = models.CharField(max_length=20, default="", blank=True)
    email = models.EmailField(default="", blank=True)
    address_1 = models.CharField(max_length=255, default="", blank=True)
    address_2 = models.CharField(max_length=255, default="", blank=True)
    city = models.CharField(max_length=255, default="", blank=True)
    province = models.CharField(max_length=255, default="", blank=True)
    postal_code = models.CharField(max_length=20, default="", blank=True)
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

    @property
    def title(self):
        return "{0} - {1}".format(self.code, self.name)

    def can_delete(self):
        return self.level != 0 and self.sanadItems.count() == 0

    def get_remain(self):
        from sanads.sanads.models import SanadItem
        bed = SanadItem.objects.filter(account__code__startswith=self.code) \
            .aggregate(Sum('bed'))['bed__sum']
        bes = SanadItem.objects.filter(account__code__startswith=self.code) \
            .aggregate(Sum('bes'))['bes__sum']

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

    def get_new_child_code(self):

        if self.level == self.TAFSILI:
            return None

        last_child = self.children.order_by('-code').first()
        if last_child:
            last_code = last_child.code[self.PARENT_PART[self.level + 1]:]
        else:
            last_code = ''
            for i in range(self.CODE_LENGTHS[self.level] - 1):
                last_code += '0'
            last_code += '1'

        code = self.code + last_code

        if code[:self.PARENT_PART[self.level + 1]] != self.code:
            from rest_framework import serializers
            raise serializers.ValidationError("تعداد حساب های این سطح پر شده است")

        return code

    @staticmethod
    def get_new_group_code(user):
        code = \
            Account.objects.inFinancialYear(user).filter(level=Account.GROUP).aggregate(Max('code'))[
                'code__max']
        code = int(code) + 1

        if code >= 10:
            from rest_framework import serializers
            raise serializers.ValidationError("تعداد حساب های این سطح پر شده است")

    @staticmethod
    def get_inventory_account(user):
        return Account.objects.inFinancialYear(user).get(code='106040001')

    @staticmethod
    def get_partners_account(user):
        return Account.objects.inFinancialYear(user).get(code='303070001')

    @staticmethod
    def get_cost_of_sold_wares_account(user):
        return Account.objects.inFinancialYear(user).get(code='701010001')
