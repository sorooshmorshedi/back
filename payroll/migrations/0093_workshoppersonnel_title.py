# Generated by Django 2.2 on 2023-01-05 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0092_auto_20230105_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshoppersonnel',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workshop_personnel', to='payroll.WorkTitle'),
        ),
    ]
