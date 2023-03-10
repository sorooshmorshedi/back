# Generated by Django 2.2 on 2022-12-12 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0026_auto_20221211_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjustment',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='university_type',
            field=models.CharField(blank=True, choices=[('st', 'دولتی'), ('op', 'آزاد'), ('np', 'غیر انتفاعی'), ('el', 'علمی کاربردی'), ('pa', 'پیام نور'), ('pr', 'پردیس خودگردان وابسته به دولت')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='personnelfamily',
            name='physical_condition',
            field=models.CharField(blank=True, choices=[('h', 'سالم'), ('p', 'بیمار'), ('m', 'نقص عضو')], max_length=1, null=True),
        ),
    ]
