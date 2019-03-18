from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True
        default_permissions = ()
        verbose_name = ''

        def __init__(self):
            model_name = self.__bases__[0]._meta.model_name
            verbose_name = self.verbose_name

            self.permissions = (
                ('create_{}'.format(model_name), 'ساخت {}'.format(verbose_name)),
                ('retrieve_{}'.format(model_name), 'مشاهده {}'.format(verbose_name)),
                ('update_{}'.format(model_name), 'ویرایش {}'.format(verbose_name)),
                ('delete_{}'.format(model_name), 'حذف {}'.format(verbose_name)),
            )
