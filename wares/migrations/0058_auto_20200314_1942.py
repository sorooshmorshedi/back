# Generated by Django 2.2 on 2020-03-14 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0014_auto_20200314_1942'),
        ('wares', '0057_auto_20200312_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='units', to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ware',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='wares', to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warebalance',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='waresBalance', to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouse',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='warehouses', to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warelevel',
            name='financial_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='wareLevels', to='companies.FinancialYear'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ware',
            name='pricingType',
            field=models.IntegerField(blank=True, choices=[(1, 'میانگین موزون'), (0, 'فایفو')], null=True),
        ),
    ]