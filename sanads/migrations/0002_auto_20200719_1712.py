# Generated by Django 2.2 on 2020-07-19 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0002_auto_20200719_1712'),
        ('sanads', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_auto_20200719_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='sanaditem',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sanaditem',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sanad_items', to='companies.FinancialYear'),
        ),
        migrations.AddField(
            model_name='sanaditem',
            name='floatAccount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sanadItems', to='accounts.FloatAccount', verbose_name='حساب شناور'),
        ),
        migrations.AddField(
            model_name='sanaditem',
            name='sanad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sanads.Sanad', verbose_name='سند'),
        ),
        migrations.AddField(
            model_name='sanad',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sanad',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sanads', to='companies.FinancialYear'),
        ),
    ]
