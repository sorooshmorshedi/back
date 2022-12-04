# Generated by Django 2.2 on 2022-12-04 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0013_auto_20221204_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='location_of_birth',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_of_birth', to='users.City'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='location_of_exportation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_of_exportation', to='users.City'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='sector_of_exportation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sector_of_exportation', to='users.City'),
        ),
    ]
