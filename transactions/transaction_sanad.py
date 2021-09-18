from helpers.auto_sanad import AutoSanad
from helpers.functions import get_object_accounts, sanad_exp
from transactions.models import Transaction


class TransactionSanad(AutoSanad):

    def get_sanad_rows(self, instance: Transaction) -> list:
        if instance.type in (Transaction.PAYMENT_GUARANTEE, Transaction.RECEIVED_GUARANTEE):
            return self.get_guarantee_sanad_rows(instance)
        else:
            return self.get_transaction_sanad_rows(instance)

    def get_guarantee_sanad_rows(self, instance: Transaction) -> list:
        rows = []
        for item in instance.items.all():
            if instance.type == Transaction.RECEIVED_GUARANTEE:
                rows.append({
                    'account': 'receivedGuarantee',
                    'bed': item.value,
                })
                rows.append({
                    'account': 'receivedGuaranteeFrom',
                    'bes': item.value,
                })
            else:
                rows.append({
                    'account': 'paymentGuarantee',
                    'bed': item.value,
                })
                rows.append({
                    'account': 'paymentGuaranteeFrom',
                    'bes': item.value,
                })
        return rows

    def get_transaction_sanad_rows(self, instance: Transaction) -> list:
        rows = []
        total_value = 0
        total_banking_operation_value = 0
        for item in instance.items.all():

            total_value += item.value

            bed = 0
            bes = 0

            row_explanation = ''
            if instance.type == Transaction.RECEIVE:
                bed = item.value
                row_explanation = sanad_exp(
                    'بابت دریافت شماره',
                    instance.code,
                    'به شماره پیگیری',
                    item.documentNumber,
                    'مورخ',
                    item.date,
                    item.explanation
                )
            else:
                bes = item.value
                if instance.type in (Transaction.PAYMENT, Transaction.BANK_TRANSFER):
                    row_explanation = sanad_exp(
                        'بابت پرداخت شماره',
                        instance.code,
                        'به شماره پیگیری',
                        item.documentNumber,
                        'مورخ',
                        item.date,
                        item.explanation
                    )
                elif instance.type == Transaction.IMPREST:
                    row_explanation = sanad_exp(
                        'بابت پرداخت تنخواه شماره',
                        instance.code,
                        'مورخ',
                        item.date,
                        'به شماره پیگیری',
                        item.documentNumber,
                        'جهت',
                        item.explanation
                    )

                if item.banking_operation_value != 0:
                    total_banking_operation_value += item.banking_operation_value
                    rows.append({
                        'bes': item.banking_operation_value,
                        **get_object_accounts(item)
                    })

            rows.append({
                'bed': bed,
                'bes': bes,
                'explanation': row_explanation,
                **get_object_accounts(item)
            })

        last_bed = 0
        last_bes = 0
        last_row_explanation = ''

        if instance.type == Transaction.RECEIVE:
            last_bes = total_value
            last_row_explanation = sanad_exp(
                'بابت واریز طی دریافت شماره',
                instance.code,
                instance.explanation
            )
        else:
            last_bed = total_value
            if instance.type in (Transaction.PAYMENT, Transaction.BANK_TRANSFER):
                last_row_explanation = sanad_exp(
                    'بابت دریافت طی شماره پرداخت',
                    instance.code,
                    'مورخ',
                    instance.date,
                    instance.explanation
                )
            elif instance.type == Transaction.IMPREST:
                last_row_explanation = sanad_exp(
                    'بابت دریافت تنخواه شماره',
                    instance.code,
                    'مورخ',
                    instance.date,
                    instance.explanation
                )

            if total_banking_operation_value != 0:
                rows.append({
                    'bed': total_banking_operation_value,
                    'account': 'paymentBankWage'
                })

        if len(instance.items.all()) != 0:
            rows.append({
                'bed': last_bed,
                'bes': last_bes,
                'explanation': last_row_explanation,
                **get_object_accounts(instance)
            })

        return rows

    def get_sanad_explanation(self):
        explanation = ''
        if self.instance.type == self.instance.RECEIVE:
            explanation = sanad_exp(
                'بابت دریافت',
                'شماره',
                self.instance.code,
                self.instance.explanation
            )
        elif self.instance.type in (self.instance.PAYMENT, self.instance.BANK_TRANSFER):
            explanation = sanad_exp(
                'بابت پرداخت',
                'شماره',
                self.instance.code,
                'مورخ',
                self.instance.date,
                self.instance.explanation
            )
        elif self.instance.type == self.instance.IMPREST:
            explanation = sanad_exp(
                'بابت پرداخت تنخواه شماره',
                self.instance.code,
                'مورخ',
                self.instance.date,
                'جهت',
                self.instance.explanation
            )
        return explanation
