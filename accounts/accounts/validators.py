from rest_framework import serializers

from accounts.accounts.models import FloatAccountRelation


class AccountValidator:

    @staticmethod
    def tafsili(data, account_key='account', float_account_key='floatAccount', cost_center_key='costCenter'):
        account = data.get(account_key)
        if not account:
            raise serializers.ValidationError("فیلد حساب اجباری می باشد")

        if account.level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")

        def has_float_account(float_account_group):
            return FloatAccountRelation.objects.inFinancialYear().filter(floatAccountGroup=float_account_group).exists()

        if account.floatAccountGroup and has_float_account(account.floatAccountGroup):
            floatAccount = data.get(float_account_key)
            if not floatAccount:
                raise serializers.ValidationError(
                    "حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if account.floatAccountGroup not in list(floatAccount.floatAccountGroups.all()):
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")

        if account.costCenterGroup and has_float_account(account.costCenterGroup):
            costCenter = data.get(cost_center_key)
            if not costCenter:
                raise serializers.ValidationError(
                    "مرکز هزینه و درآمد برای حساب های دارای گروه گروه مرکز هزینه و درآمد باید انتخاب گردد")
            if account.costCenterGroup not in list(costCenter.floatAccountGroups.all()):
                raise serializers.ValidationError(
                    "مرکز هزینه و درآمد انتخاب شده باید مطعلق به گروه مرکز هزینه و درآمد حساب باشد")
