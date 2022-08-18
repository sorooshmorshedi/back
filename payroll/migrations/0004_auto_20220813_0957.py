# Generated by Django 2.2 on 2022-08-13 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0003_auto_20220811_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='hrletter',
            name='is_template',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hr_letter', to='payroll.Contract'),
        ),
    ]