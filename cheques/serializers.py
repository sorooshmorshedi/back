from accounts.accounts.serializers import AccountListRetrieveSerializer, FloatAccountSerializer
from cheques.models import *
from sanads.sanads.serializers import SanadListRetrieveSerializer


class StatusChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatusChange
        fields = '__all__'

    def validate(self, data):
        if 'bedAccount' not in data or 'besAccount' not in data:
            raise serializers.ValidationError("حساب بدهکار و یا بستانکار انتخاب نشده است")

        if ('bedAccount' in data and data['bedAccount'].level != 3) or ('besAccount' in data and data['besAccount'].level != 3):
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")

        if 'bedAccount' in data and data['bedAccount'].floatAccountGroup:
            if 'bedFloatAccount' not in data:
                raise serializers.ValidationError("حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['bedFloatAccount'].floatAccountGroup != data['bedAccount'].floatAccountGroup:
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")
        if 'besAccount' in data and data['besAccount'].floatAccountGroup:
            if 'besFloatAccount' not in data:
                raise serializers.ValidationError("حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['besFloatAccount'].floatAccountGroup != data['besAccount'].floatAccountGroup:
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")

        if data['bedAccount'] == data['besAccount']:
            raise serializers.ValidationError("حساب بدهکار و بستانکار نمی تواند یکی باشد")

        if data['fromStatus'] == 'blank':
            if data['toStatus'] != 'notPassed':
                raise serializers.ValidationError("ابتدا چک را ثبت کنید")
            else:
                cheque = data['cheque']
                if not cheque.value:
                    raise serializers.ValidationError("لطفا مبلغ چک را وارد کنید")
                if not cheque.due:
                    raise serializers.ValidationError("لطفا تاریخ سر رسید چک را وارد کنید")
                if not cheque.date:
                    raise serializers.ValidationError("لطفا تاریخ دریافت/پرداخت چک را وارد کنید")

        if data['fromStatus'] == data['toStatus']:
            raise serializers.ValidationError("لطفا وضعیت جدیدی برای تغییر انتخاب کنید")

        return data

    def create(self, validated_data):
        if 'data' not in validated_data and not validated_data['sanad']:
            sanad = Sanad(code=Sanad.objects.latest('code').code + 1, date=validated_data['date'], createType='auto')
            sanad.save()
            validated_data['sanad'] = sanad
        return super(StatusChangeSerializer, self).create(validated_data)


class StatusChangeListRetrieveSerializer(serializers.ModelSerializer):
    sanad = SanadListRetrieveSerializer(read_only=True, many=False)

    class Meta:
        model = StatusChange
        fields = '__all__'


class ChequeSerializer(serializers.ModelSerializer):
    # title = serializers.SerializerMethodField()
    #
    # def get_title(self, obj):
    #     return obj.ser+ ' - ' + obj.name

    class Meta:
        model = Cheque
        fields = ('id', 'serial', 'account', 'floatAccount', 'sanadItem', 'value', 'due', 'date', 'explanation')

    def validate(self, data):
        if 'account' not in data or not data['account']:
            raise serializers.ValidationError("لطفا حساب دریافت کننده/پرداخت کننده را مشخص کنید")
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")
        if data['account'].floatAccountGroup:
            if 'floatAccount' not in data:
                raise serializers.ValidationError("حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['floatAccount'].floatAccountGroup != data['account'].floatAccountGroup:
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")

        return data

    def create(self, validated_data):
        data = validated_data.copy()
        data['status'] = 'blank'
        data['type'] = 'received'
        return super(ChequeSerializer, self).create(validated_data=data)


class ChequeListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    statusChanges = StatusChangeListRetrieveSerializer(read_only=True, many=True)

    class Meta:
        model = Cheque
        fields = '__all__'


class ChequebookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chequebook
        fields = '__all__'

    def validate(self, data):
        if data['account'].level != 3:
            raise serializers.ValidationError("حساب انتخابی باید حتما از سطح آخر باشد")
        if data['account'].floatAccountGroup:
            if 'floatAccount' not in data:
                raise serializers.ValidationError("حساب تفضیلی شناور برای حساب های دارای گروه حساب تفضیلی شناور باید انتخاب گردد")
            if data['floatAccount'].floatAccountGroup != data['account'].floatAccountGroup:
                raise serializers.ValidationError("حساب شناور انتخاب شده باید مطعلق به گروه حساب شناور حساب باشد")

        return data


class ChequebookListRetrieveSerializer(ChequebookSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    cheques = ChequeListRetrieveSerializer(read_only=True, many=True)

    class Meta(ChequebookSerializer.Meta):
        pass


