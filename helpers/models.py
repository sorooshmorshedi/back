from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True
        default_permissions = ()
        verbose_name = ''

        # permissions = (
        #     ('create_', 'ساخت '),
        #     ('retrieve_', 'مشاهده '),
        #     ('update_', 'ویرایش '),
        #     ('delete_', 'حذف '),
        # )
