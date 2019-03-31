from decimal import Decimal
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from factors.models import Factor
from sanads.sanads.models import Sanad
from sanads.transactions.models import Transaction


class BillListView(APIView):

    def get_queryset(self):
        return Sanad.objects.order_by('-code')\
            .prefetch_related('items') \
            .prefetch_related('factor__items__ware__unit') \
            .prefetch_related('transaction__items__type') \
            .prefetch_related('transaction__items__cheque')

    def get(self, request, *args, **kwargs):
        try:
            account_id = request.GET['account_id']
            account_id = int(account_id)
        except MultiValueDictKeyError:
            return Response(data={'non_field_errors': ['id حساب وارد نشده است']})

        queryset = self.get_queryset()

        limit = 1000
        data = []
        # TODO make this for chunk by chunk
        for sanad in queryset.all():
            if len(data) >= limit:
                break
            try:
                self.append_factor_items(data, sanad, account_id)
            except Factor.DoesNotExist:
                try:
                    self.append_transaction_items(data, sanad, account_id)
                except Transaction.DoesNotExist:
                    self.append_sanad_items(data, sanad, account_id)

        if len(data):
            BED = 'بدهکار'
            BES = 'بستانکار'
            if data[0]['bed'] != 0:
                remain = data[0]['bed']
                remain_type = BED
            else:
                remain = data[0]['bes']
                remain_type = BES
            data[0]['remain'] = remain
            data[0]['remain_type'] = remain_type
            for i in range(1, len(data)):
                if data[i-1]['remain_type'] == BED:
                    if data[i]['bed'] != 0:
                        data[i]['remain'] = data[i-1]['remain'] + data[i]['bed']
                    else:
                        data[i]['remain'] = data[i-1]['remain'] - data[i]['bes']
                else:
                    if data[i]['bes'] != 0:
                        data[i]['remain'] = data[i-1]['remain'] + Decimal(data[i]['bes'])
                    else:
                        data[i]['remain'] = data[i-1]['remain'] - Decimal(data[i]['bed'])
                if data[i]['remain'] < 0:
                    data[i]['remain'] = -data[i]['remain']
                    data[i]['remain_type'] = BED if data[i-1]['remain_type'] == BES else BES
                else:
                    data[i]['remain_type'] = data[i-1]['remain_type']

        return Response(data=data, status=status.HTTP_200_OK)

    def append_factor_items(self, data, sanad, account_id):
        factor = sanad.factor
        if factor.account_id != account_id:
            return
        for item in factor.items.all():
            value = item.totalValue
            valueType = 'bes' if factor.type in ('buy', 'backFromSale') else 'bed'
            bed = bes = 0
            if valueType == 'bed':
                bed = value
            else:
                bes = value

            row = {
                'form_name': factor.label,
                'form_id': factor.id,
                'type': factor.type,
                'date': str(factor.date),
                'sanad': sanad.id,
                'explanation': "نام کالا: {}, تعداد: {} {}, قیمت واحد: {}, تخفیف: {}, توضیحات: {}".format(item.ware, item.count, item.ware.unit,
                                                          item.fee, item.discount, item.explanation),
                'bed': bed,
                'bes': bes
            }

            data.append(row)

    def append_transaction_items(self, data, sanad, account_id):
        transaction = sanad.transaction
        if transaction.account_id != account_id:
            return
        for item in transaction.items.all():
            value = item.value
            valueType = 'bes' if transaction.type == 'received' else 'bed'
            bed = bes = 0
            if valueType == 'bed':
                bed = value
            else:
                bes = value
            row = {
                'form_name': transaction.label,
                'form_id': transaction.id,
                'type': transaction.type,
                'date': str(transaction.date),
                'sanad': sanad.id,
                'bed': bed,
                'bes': bes
            }
            if item.cheque:
                row['explanation'] = "شماره چک: {}, تاریخ سررسید: {}, توضیحات: {}".format(item.cheque.serial, item.cheque.due, item.explanation)
            else:
                row['explanation'] = "نوع: {}, تاریخ: {}, شماره مستند: {}, توضیحات: {}".format(item.type, item.date, item.documentNumber, item.explanation)
            # serialized = self.serializer_class(data=row)
            # serialized.is_valid()
            # data.append(serialized.data)
            data.append(row)

    def append_sanad_items(self, data, sanad, account_id):
        for item in sanad.items.all():
            if item.account_id != account_id:
                continue
            bed = bes = 0
            if item.valueType == 'bed':
                bed = item.value
            else:
                bes = item.value

            row = {
                'form_name': 'سند',
                'type': sanad.type,
                'date': str(sanad.date),
                'sanad': sanad.id,
                'explanation': "{}".format(item.explanation),
                'bed': bed,
                'bes': bes
            }

            # serialized = self.serializer_class(data=row)
            # serialized.is_valid()
            # data.append(serialized.data)
            data.append(row)
