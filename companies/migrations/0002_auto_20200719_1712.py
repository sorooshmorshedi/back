# Generated by Django 2.2 on 2020-07-19 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sanads', '0001_initial'),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialyear',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='financialyear',
            name='currentEarningsClosingSanad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='financialYearAsCurrentEarningsClosingSanad', to='sanads.Sanad'),
        ),
        migrations.AddField(
            model_name='financialyear',
            name='openingSanad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='financialYearAsOpeningSanad', to='sanads.Sanad'),
        ),
        migrations.AddField(
            model_name='financialyear',
            name='permanentsClosingSanad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='financialYearAsPermanentsClosingSanad', to='sanads.Sanad'),
        ),
        migrations.AddField(
            model_name='financialyear',
            name='temporaryClosingSanad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='financialYearAsTemporaryClosingSanad', to='sanads.Sanad'),
        ),
        migrations.AddField(
            model_name='company',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]