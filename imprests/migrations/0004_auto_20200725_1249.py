# Generated by Django 2.2 on 2020-07-25 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imprests', '0003_auto_20200719_1719'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imprestsettlement',
            options={'default_permissions': (), 'ordering': ['-code'], 'permissions': (('get.imprestSettlement', 'مشاهده تسویه تنخواه'), ('create.imprestSettlement', 'تعریف تسویه تنخواه'), ('update.imprestSettlement', 'ویرایش تسویه تنخواه'), ('delete.imprestSettlement', 'حذف تسویه تنخواه'), ('getOwn.imprestSettlement', 'مشاهده تسویه تنخواه های خود'), ('updateOwn.imprestSettlement', 'ویرایش تسویه تنخواه های خود'), ('deleteOwn.imprestSettlement', 'حذف تسویه تنخواه های خود'))},
        ),
    ]
