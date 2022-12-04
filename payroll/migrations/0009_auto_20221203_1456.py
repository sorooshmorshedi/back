# Generated by Django 2.2 on 2022-12-03 11:26

from django.db import migrations, models
import payroll.functions


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0008_auto_20221203_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractrow',
            name='assignor_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contractrow',
            name='assignor_national_code',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[payroll.functions.is_shenase_meli]),
        ),
        migrations.AlterField(
            model_name='contractrow',
            name='assignor_workshop_code',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='contractrow',
            name='contract_row',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='contractrow',
            name='status',
            field=models.CharField(choices=[('a', 'فعال'), ('n', 'غیر فعال')], default='n', max_length=1),
        ),
    ]
