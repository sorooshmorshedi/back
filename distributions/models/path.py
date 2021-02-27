from django.db import models
from companies.models import FinancialYear
from helpers.db import get_empty_array
from helpers.models import BaseModel, TreeMixin


class Path(BaseModel, TreeMixin):
    from distributions.models import Visitor

    CODE_LENGTHS = [2, 2, 2, 2, 2]

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    visitors = models.ManyToManyField(Visitor, related_name='paths', blank=True, default=get_empty_array)

    class Meta(BaseModel.Meta):
        ordering = ['code', ]
        backward_financial_year = True
        permission_basename = 'path'
        permissions = (
            ('get.path', 'مشاهده مسیر ها'),

            ('create.path0', 'تعریف استان'),
            ('update.path0', 'ویرایش استان'),
            ('delete.path0', 'حذف استان'),

            ('create.path1', 'تعریف شهر'),
            ('update.path1', 'ویرایش شهر'),
            ('delete.path1', 'حذف شهر'),

            ('create.path2', 'تعریف منطقه'),
            ('update.path2', 'ویرایش منطقه'),
            ('delete.path2', 'حذف منطقه'),

            ('create.path3', 'تعریف محله'),
            ('update.path3', 'ویرایش محله'),
            ('delete.path3', 'حذف محله'),

            ('create.path4', 'تعریف خیابان'),
            ('update.path4', 'ویرایش خیابان'),
            ('delete.path4', 'حذف خیابان'),

            ('getOwn.path', 'مشاهده مسیر ها خود'),

            ('updateOwn.path0', 'ویرایش استان خود'),
            ('deleteOwn.path0', 'حذف استان خود'),

            ('updateOwn.path1', 'ویرایش شهر خود'),
            ('deleteOwn.path1', 'حذف شهر خود'),

            ('updateOwn.path2', 'ویرایش منطقه خود'),
            ('deleteOwn.path2', 'حذف منطقه خود'),

            ('updateOwn.path3', 'ویرایش محله خود'),
            ('deleteOwn.path3', 'حذف محله خود'),

            ('updateOwn.path4', 'ویرایش خیابان خود'),
            ('deleteOwn.path4', 'حذف خیابان خود'),
        )
