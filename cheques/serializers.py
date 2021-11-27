from rest_framework import serializers

from accounts.accounts.serializers import AccountRetrieveSerializer, FloatAccountSerializer, AccountSimpleSerializer
from accounts.accounts.validators import AccountValidator
from cheques.models.ChequeModel import Cheque, STATUS_TREE, BLANK, REVOKED, NOT_PASSED, PASSED, TRANSFERRED, CASHED, IN_FLOW
from cheques.models.ChequebookModel import Chequebook
from cheques.models.StatusChangeModel import StatusChange
from helpers.serializers import validate_required_fields
from sanads.serializers import SanadRetrieveSerializer


class StatusChangeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusChange
        fields = '__all__'

    def validate(self, data):
        cheque = data['cheque']
        from_status = data['fromStatus']
        to_status = data['toStatus']

        if cheque.is_paid:
            status_tree = STATUS_TREE['p']
        else:
            status_tree = STATUS_TREE['r']

        valid_destinations = status_tree.get(from_status)
        if valid_destinations:
            if to_status not in valid_destinations:
                raise serializers.ValidationError("تغییر وضعیت از {} به {} امکان پذیر نمی باشد".format(from_status, to_status))
        else:
            raise serializers.ValidationError("امکان تغییر وضعیت {} وجود ندارد".format(from_status))

        if cheque.status == BLANK and to_status == REVOKED:
            validate_required_fields(data, ['explanation'])
        else:
            if 'bedAccount' not in data or 'besAccount' not in data:
                raise serializers.ValidationError("حساب بدهکار و یا بستانکار انتخاب نشده است")

            if data['bedAccount'] == data['besAccount']:
                raise serializers.ValidationError("حساب بدهکار و بستانکار نمی تواند یکی باشد")

            if not cheque.value:
                raise serializers.ValidationError("لطفا مبلغ چک را وارد کنید")
            if not cheque.due:
                raise serializers.ValidationError("لطفا تاریخ سر رسید چک را وارد کنید")
            if not cheque.date:
                raise serializers.ValidationError("لطفا تاریخ دریافت/پرداخت چک را وارد کنید")

        if to_status in [PASSED, TRANSFERRED, CASHED, IN_FLOW]:
            validate_required_fields(data, ['bedAccount', 'besAccount'])

        return data


class StatusChangeListRetrieveSerializer(serializers.ModelSerializer):
    sanad = serializers.SerializerMethodField()

    def get_sanad(self, obj: StatusChange):
        if obj.sanad:
            return SanadRetrieveSerializer(obj.sanad).data
        if hasattr(obj.cheque, 'transactionItem'):
            return SanadRetrieveSerializer(obj.cheque.transactionItem.transaction.sanad).data

    class Meta:
        model = StatusChange
        fields = '__all__'


class ChequebookCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chequebook
        fields = '__all__'
        read_only_fields = ('financial_year', 'code',)

    def validate(self, data):

        AccountValidator.tafsili(data)

        if self.instance:
            for cheque in self.instance.cheques.all():
                if cheque.status != 'blank':
                    raise serializers.ValidationError("برای ویرایش دسته چک، باید وضعیت همه چک های آن سفید باشد")

        return super(ChequebookCreateUpdateSerializer, self).validate(data)


class ChequebookListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountSimpleSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    costCenter = FloatAccountSerializer(read_only=True, many=False)

    class Meta:
        model = Chequebook
        fields = '__all__'


class ChequeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheque
        fields = '__all__'
        read_only_fields = ('financial_year', 'status')

    def validate(self, data):

        AccountValidator.tafsili(data)

        is_paid = data.get('is_paid', False) == True

        if self.instance:
            cheque: Cheque = self.instance
            if cheque.statusChanges.count() >= 1:
                raise serializers.ValidationError("چک غیر قابل ویرایش می باشد")

        return data

    def update(self, instance: Cheque, validated_data):
        if instance.is_paid:
            validated_data.pop('serial')
            validated_data.pop('is_paid')

        return super(ChequeCreateUpdateSerializer, self).update(instance, validated_data)


class ChequeRetrieveSerializer(serializers.ModelSerializer):
    account = AccountRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    costCenter = FloatAccountSerializer(read_only=True, many=False)
    statusChanges = StatusChangeListRetrieveSerializer(read_only=True, many=True)

    chequebook = ChequebookListRetrieveSerializer(read_only=True, many=False)

    title = serializers.SerializerMethodField()

    # transaction = serializers.IntegerField(source="transactionItem.transaction.id")
    # transactionSanad = SanadListRetrieveSerializer(source="transactionItem.transaction.id")

    def get_title(self, obj):
        if obj.chequebook:
            return "{0} - {1}".format(obj.chequebook.explanation[0:50], obj.serial)
        else:
            return "{0} - {1}".format(obj.explanation[0:50], obj.serial)

    class Meta:
        model = Cheque
        fields = '__all__'
