# Generated by Django 2.2 on 2020-07-25 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0003_auto_20200721_1201'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ware',
            options={'default_permissions': (), 'ordering': ['code'], 'permissions': (('get.ware', 'مشاهده کالا'), ('create.ware', 'تعریف کالا'), ('update.ware', 'ویرایش کالا'), ('delete.ware', 'حذف کالا'), ('getOwn.ware', 'مشاهده کالا های خود'), ('updateOwn.ware', 'ویرایش کالا های خود'), ('deleteOwn.ware', 'حذف کالا های خود'))},
        ),
    ]
