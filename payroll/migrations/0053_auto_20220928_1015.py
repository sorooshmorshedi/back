# Generated by Django 2.2 on 2022-09-28 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0052_auto_20220928_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='hrletter',
            name='eydi_padash_use_insurance',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='hrletter',
            name='eydi_padash_use_tax',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='hrletter',
            name='haghe_sanavat_use_insurance',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='hrletter',
            name='haghe_sanavat_use_tax',
            field=models.BooleanField(default=True),
        ),
    ]
