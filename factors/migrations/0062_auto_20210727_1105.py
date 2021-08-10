# Generated by Django 2.2 on 2021-07-27 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0031_auto_20210718_1141'),
        ('factors', '0061_auto_20210719_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='factorsaggregatedsanad',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factorsaggregatedsanad',
            name='type',
            field=models.CharField(choices=[('buy', 'خرید'), ('sale', 'فروش'), ('backFromBuy', 'بازگشت از خرید'), ('backFromSale', 'بازگشت از فروش'), ('fpi', 'موجودی اول دوره'), ('it', 'وارده از انتقال'), ('ot', 'صادره با انتقال'), ('cw', 'حواله کالای مصرفی'), ('ia', 'رسید تعدیل انبار'), ('oa', 'حواله تعدیل انبار'), ('rc', 'رسید'), ('rm', 'حواله'), ('p', 'تولید')], default='buy', max_length=15),
            preserve_default=False,
        ),
    ]