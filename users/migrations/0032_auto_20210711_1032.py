# Generated by Django 2.2 on 2021-07-11 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_auto_20210629_1526'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': (('create.city', 'تعریف شهر'), ('get.city', 'مشاهده شهر'), ('update.city', 'ویرایش شهر'), ('delete.city', 'حذف شهر'), ('getOwn.city', 'مشاهده شهر های خود'), ('updateOwn.city', 'ویرایش شهر های خود'), ('deleteOwn.city', 'حذف شهر های خود'))},
        ),
    ]