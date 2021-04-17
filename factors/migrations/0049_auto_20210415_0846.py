# Generated by Django 2.2 on 2021-04-15 04:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0048_auto_20210411_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='is_pre_factor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='factoritem',
            name='preFactorItem',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='factorItem', to='factors.FactorItem'),
        ),
        migrations.AlterField(
            model_name='factor',
            name='type',
            field=models.CharField(choices=[('buy', 'خرید'), ('sale', 'فروش'), ('backFromBuy', 'بازگشت از خرید'), ('backFromSale', 'بازگشت از فروش'), ('fpi', 'موجودی اول دوره'), ('it', 'وارده از انتقال'), ('ot', 'صادره با انتقال'), ('cw', 'حواله کالای مصرفی'), ('ia', 'رسید تعدیل انبار'), ('oa', 'حواله تعدیل انبار'), ('rc', 'رسید'), ('rm', 'حواله')], max_length=15),
        ),
    ]
