# Generated by Django 2.2 on 2020-03-15 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sanads', '0014_auto_20200310_1326'),
        ('companies', '0014_auto_20200314_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialyear',
            name='closingSanad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='financialYearAsClosingSanad', to='sanads.Sanad'),
        ),
    ]
