from rest_framework import serializers

from accounts.accounts.serializers import AccountListRetrieveSerializer, FloatAccountSerializer
from cheques.models.ChequeModel import Cheque
from cheques.models.ChequebookModel import Chequebook
from cheques.models.StatusChangeModel import StatusChange
from sanads.sanads.serializers import SanadListRetrieveSerializer


class StatusChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusChange
        fields = '__all__'

    def validate(self, data):
        cheque = data['cheque']

        if cheque.statusChanges.count() > 1:
            raise serializers.ValidationError("ابتدا تغییر وضعیت های چک را پاک کنید")

        if 'bedAccount' not in data or 'besAccount' not in data:
            raise serializers.ValidationError("حساب بدهکار و یا بستانکار انتخاب نشده است")

        if ('bedAccount' in data and data['bedAccount'].level != 3) or (
                'besAccount' in data and data['besAccount'].level != 3):
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")

        if 'bedAccount' in data and data['bedAccount'].floatAccountGroup:
            if 'bedFloatAccount' not in data:
                raise serializers.ValidationError(
                    "حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['bedAccount'].floatAccountGroup not in list(data['bedFloatAccount'].floatAccountGroups.all()):
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")
        if 'besAccount' in data and data['besAccount'].floatAccountGroup:
            if 'besFloatAccount' not in data:
                raise serializers.ValidationError(
                    "حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['bedAccount'].floatAccountGroup not in list(data['bedFloatAccount'].floatAccountGroups.all()):
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")

        if data['bedAccount'] == data['besAccount']:
            raise serializers.ValidationError("حساب بدهکار و بستانکار نمی تواند یکی باشد")

        if data['fromStatus'] == 'blank':
            if data['toStatus'] != 'notPassed':
                raise serializers.ValidationError("ابتدا چک را ثبت کنید")
            else:
                if not cheque.value:
                    raise serializers.ValidationError("لطفا مبلغ چک را وارد کنید")
                if not cheque.due:
                    raise serializers.ValidationError("لطفا تاریخ سر رسید چک را وارد کنید")
                if not cheque.date:
                    raise serializers.ValidationError("لطفا تاریخ دریافت/پرداخت چک را وارد کنید")

        if data['fromStatus'] == data['toStatus']:
            raise serializers.ValidationError("لطفا وضعیت جدیدی برای تغییر انتخاب کنید")

        return data


class StatusChangeListRetrieveSerializer(serializers.ModelSerializer):
    sanad = SanadListRetrieveSerializer(read_only=True, many=False)

    class Meta:
        model = StatusChange
        fields = '__all__'


class ChequebookCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chequebook
        fields = '__all__'
        read_only_fields = ('financial_year', 'code',)

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")
        if data['account'].floatAccountGroup:
            if 'floatAccount' not in data:
                raise serializers.ValidationError(
                    "حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['account'].floatAccountGroup not in list(data['floatAccount'].floatAccountGroups.all()):
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")

        if self.instance:
            for cheque in self.instance.cheques.all():
                if cheque.status != 'blank':
                    raise serializers.ValidationError("برای ویرایش دسته چک، باید وضعیت همه چک های آن سفید باشد")

        return data


class ChequebookListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)

    class Meta:
        model = Chequebook
        fields = '__all__'


class ChequeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheque
        fields = '__all__'
        read_only_fields = ('financial_year', 'status')

    def validate(self, data):

        if 'account' not in data or not data['account']:
            raise serializers.ValidationError("لطفا حساب دریافت کننده/پرداخت کننده را مشخص کنید")
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")
        if data['account'].floatAccountGroup:
            if 'floatAccount' not in data:
                raise serializers.ValidationError(
                    "حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['account'].floatAccountGroup not in list(data['floatAccount'].floatAccountGroups.all()):
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")

        received_or_paid = data.get('received_or_paid')

        if received_or_paid not in (Cheque.RECEIVED, Cheque.PAID):
            raise serializers.ValidationError("لطفا نوع چک (پرداختی یا دریافتی) را مشخص کنید")

        if self.instance:
            if self.instance.chequebook and received_or_paid != Cheque.PAID:
                raise serializers.ValidationError("نوع چک غیر قابل قبول است")

        return data

    def update(self, instance: Cheque, validated_data):
        if instance.received_or_paid == Cheque.PAID:
            validated_data.pop('serial')
            validated_data.pop('received_or_paid')

        return super(ChequeCreateUpdateSerializer, self).update(instance, validated_data)


class ChequeListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    statusChanges = StatusChangeListRetrieveSerializer(read_only=True, many=True)

    chequebook = ChequebookListRetrieveSerializer(read_only=True, many=False)

    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        if obj.chequebook:
            return "{0} - {1}".format(obj.chequebook.explanation[0:50], obj.serial)
        else:
            return "{0} - {1}".format(obj.explanation[0:50], obj.serial)

    class Meta:
        model = Cheque
        fields = '__all__'
