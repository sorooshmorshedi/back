from helpers.auto_sanad import AutoSanad
from helpers.functions import get_object_accounts, sanad_exp
from transactions.models import Transaction


class StatusChangeSanad(AutoSanad):

    def get_sanad_rows(self, instance: StatusChangeSanad) -> list:
        data = {
            'cheque': self.id,
            'fromStatus': self.status,
            'toStatus': to_status,
            'financial_year': user.active_financial_year.id,
            'date': date,
            'explanation': explanation
        }

        if sanad:
            data['sanad'] = sanad.id

        lastFloatAccount = None
        lastCostCenter = None

        if not self.is_paid:

            data['besAccount'] = self.lastAccount.id
            if self.lastFloatAccount:
                data['besFloatAccount'] = self.lastFloatAccount.id
            if self.lastCostCenter:
                data['besCostCenter'] = self.lastCostCenter.id

            if to_status == 'revoked' or to_status == 'bounced':
                lastAccount = self.account
                data['bedAccount'] = self.account.id
                if self.floatAccount:
                    lastFloatAccount = self.floatAccount
                    data['bedFloatAccount'] = self.floatAccount.id
                if self.costCenter:
                    lastCostCenter = self.costCenter
                    data['bedCostCenter'] = self.costCenter.id

            elif to_status == 'notPassed':
                defaultAccount = DefaultAccount.get('receivedCheque')
                lastAccount = defaultAccount.account
                lastFloatAccount = defaultAccount.floatAccount
                lastCostCenter = defaultAccount.costCenter
                data['bedAccount'] = lastAccount.id

            else:
                lastAccount = account
                data['bedAccount'] = account.id
                if floatAccount:
                    lastFloatAccount = floatAccount
                    data['bedFloatAccount'] = floatAccount.id
                if costCenter:
                    lastCostCenter = costCenter
                    data['bedCostCenter'] = costCenter.id

        else:

            if self.status == 'blank' and to_status == 'revoked':
                lastAccount = self.lastAccount
                lastFloatAccount = self.lastFloatAccount
                lastCostCenter = self.lastCostCenter
            else:

                data['bedAccount'] = self.lastAccount.id
                if self.lastFloatAccount:
                    data['bedFloatAccount'] = self.lastFloatAccount.id
                if self.lastCostCenter:
                    data['bedCostCenter'] = self.lastCostCenter.id

                if to_status == 'revoked' or to_status == 'bounced':
                    lastAccount = self.account
                    data['besAccount'] = self.account.id
                    if self.floatAccount:
                        lastFloatAccount = self.floatAccount
                        data['besFloatAccount'] = self.floatAccount.id
                    if self.costCenter:
                        lastCostCenter = self.costCenter
                        data['besCostCenter'] = self.costCenter.id

                elif to_status == 'passed':
                    lastAccount = self.chequebook.account
                    data['besAccount'] = self.chequebook.account.id
                    if self.chequebook.floatAccount:
                        lastFloatAccount = self.chequebook.floatAccount
                        data['besFloatAccount'] = self.chequebook.floatAccount.id
                    if self.chequebook.costCenter:
                        lastCostCenter = self.chequebook.costCenter
                        data['besCostCenter'] = self.chequebook.costCenter.id

                elif to_status == 'notPassed':
                    defaultAccount = DefaultAccount.get('paidCheque')
                    lastAccount = defaultAccount.account
                    lastFloatAccount = defaultAccount.floatAccount
                    lastCostCenter = defaultAccount.costCenter

                    data['besAccount'] = lastAccount.id
                    if lastFloatAccount:
                        data['besFloatAccount'] = lastFloatAccount.id
                    if lastCostCenter:
                        data['besCostCenter'] = lastCostCenter.id

                else:
                    lastAccount = account
                    data['besAccount'] = account.id
                    if floatAccount:
                        lastFloatAccount = floatAccount
                        data['besFloatAccount'] = floatAccount.id
                    if costCenter:
                        lastCostCenter = costCenter
                        data['besCostCenter'] = costCenter.id

        from cheques.serializers import StatusChangeSerializer
        serialized = StatusChangeSerializer(data=data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        self.lastAccount = lastAccount
        self.lastFloatAccount = lastFloatAccount
        self.lastCostCenter = lastCostCenter
        self.status = to_status
        self.save()

        return serialized.instance

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
