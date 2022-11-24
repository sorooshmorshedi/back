# Generated by Django 2.2 on 2021-12-27 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracting', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contract',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': (('get.contract', 'مشاهده قرارداد'), ('create.contract', 'تعریف قرارداد'), ('update.contract', 'ویرایش قرارداد'), ('delete.contract', 'حذف قرارداد'), ('getOwn.contract', 'مشاهده قرارداد های خود'), ('updateOwn.contract', 'ویرایش قرارداد های خود'), ('deleteOwn.contract', 'حذف قرارداد های خود')), 'verbose_name': 'Contract'},
        ),
        migrations.AlterModelOptions(
            name='tender',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': (('get.tender', 'مشاهده مناقصه'), ('create.tender', 'تعریف مناقصه'), ('update.tender', 'ویرایش مناقصه'), ('delete.tender', 'حذف مناقصه'), ('getOwn.tender', 'مشاهده مناقصه خود'), ('updateOwn.tender', 'ویرایش مناقصه خود'), ('deleteOwn.tender', 'حذف مناقصه خود')), 'verbose_name': 'Tender'},
        ),
    ]
