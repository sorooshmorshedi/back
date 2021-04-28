# Generated by Django 2.2 on 2021-04-28 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0020_auto_20210316_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exportverifier',
            name='form',
            field=models.CharField(choices=[('s', 'سند'), ('fb', 'فاکتور خرید'), ('fs', 'فاکتور فروش'), ('fbfb', 'فاکتور برگشت از خرید'), ('fbfs', 'فاکتور برگشت از فروش'), ('tr', 'دریافت'), ('tp', 'پرداخت'), ('t', 'انتقال'), ('cwr', 'حواله کالای مصرفی'), ('fpi', 'موجودی اول دوره'), ('ia', 'رسید تعدیل انبار'), ('oa', 'حواله تعدیل انبار'), ('pfb', 'پیش فاکتور خرید'), ('pfs', 'پیش فاکتور فروش'), ('frc', 'رسید'), ('frm', 'حواله')], max_length=4),
        ),
    ]
