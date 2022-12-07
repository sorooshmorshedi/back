# Generated by Django 2.2 on 2022-12-07 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0007_auto_20221207_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnelfamily',
            name='physical_condition',
            field=models.CharField(blank=True, choices=[('h', 'سالم'), ('p', 'بیمار'), ('m', 'نقض عضو')], max_length=1, null=True),
        ),
    ]
