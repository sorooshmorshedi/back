# Generated by Django 2.2 on 2022-12-06 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_city_code'),
        ('payroll', '0004_personnel_location_of_foreign_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='city_of_personnel', to='users.City'),
        ),
    ]