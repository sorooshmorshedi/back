# Generated by Django 2.2 on 2023-02-02 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0113_workshop_save_leave_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='save_leave_limit',
            field=models.IntegerField(default=26),
        ),
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='save_leave_limit',
            field=models.IntegerField(default=26),
        ),
    ]
