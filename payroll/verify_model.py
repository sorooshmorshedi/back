from django.db import models


class VerifyMixin(models.Model):
    is_verified = models.BooleanField(default=False)

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
