# Generated by Django 2.2 on 2019-05-23 00:28

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0018_remove_factoritem_output_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', django_jalali.db.models.jDateField()),
                ('created_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
                ('updated_at', django_jalali.db.models.jDateField(blank=True, editable=False)),
                ('explanation', models.CharField(blank=True, max_length=255)),
                ('input_factor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='input_transfer', to='factors.Factor')),
                ('output_factor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='output_transfer', to='factors.Factor')),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]
