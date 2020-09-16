# Generated by Django 2.2 on 2020-09-15 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0012_auto_20200901_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='type',
            field=models.CharField(choices=[('buy', 'خرید'), ('sale', 'فروش'), ('backFromBuy', 'بازگشت از خرید'), ('backFromSale', 'بازگشت از فروش'), ('fpi', 'موجودی اول دوره'), ('it', 'وارده از انتقال'), ('ot', 'صادره با انتقال'), ('cw', 'حواله کالای مصرفی'), ('ia', 'رسید تعدیل انبار'), ('oa', 'حواله تعدیل انبار')], max_length=15),
        ),
    ]