from rest_framework import serializers


class AccountValidator:

    @staticmethod
    def tafsili(data, account_key='account', float_account_key='floatAccount'):
        account = data.get(account_key)
        if not account:
            raise serializers.ValidationError("فیلد حساب اجباری می باشد")

        if account.level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")
        if account.floatAccountGroup:
            floatAccount = data.get(float_account_key)
            if not floatAccount:
                raise serializers.ValidationError(
                    "حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if account.floatAccountGroup not in list(floatAccount.floatAccountGroups.all()):
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")