# Generated by Django 2.2 on 2020-04-19 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0018_auto_20200413_1028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'permissions': (('get.account', 'مشاهده حساب ها'), ('post.account', 'تعریف حساب'), ('put.account', 'ویرایش حساب'), ('delete.account', 'حذف حساب'))},
        ),
    ]
