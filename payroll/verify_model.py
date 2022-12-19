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
