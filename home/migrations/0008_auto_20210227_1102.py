# Generated by Django 2.2 on 2021-02-27 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20201107_1531'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='option',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': (('get.option', 'مشاهده تنظیمات'), ('update.option', 'ویرایش تنظیمات'))},
        ),
    ]
