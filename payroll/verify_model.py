from django.db import models


class VerifyMixin(models.Model):
    is_verified = models.BooleanField(default=False)
    un_editable = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def verify_display(self):
        if self.is_verified == None:
            return ' - '
        elif self.is_verified:
            return 'نهایی'
        else:
            return 'اولیه'

    @property
    def edit_display(self):
        if self.un_editable == None:
            return ' - '
        elif self.un_editable:
            return 'غیر قابل ویرایش'
        else:
            return 'قابل ویرایش'


    @staticmethod
    def with_comma(input_amount, no_minus=False):
        if input_amount != 0:
            amount = str(round(input_amount))[::-1]
            loop = int(len(amount) / 3)
            if len(amount) < 4:
                return str(round(input_amount))
            else:
                counter = 0
                for i in range(1, loop + 1):
                    index = (i * 3) + counter
                    counter += 1
                    amount = amount[:index] + ',' + amount[index:]
            if amount[-1] == ',':
                amount = amount[:-1]
            if no_minus:
                return amount[::-1].replace('-', '')
            res = amount[::-1]
            return res
        else:
            return 0
