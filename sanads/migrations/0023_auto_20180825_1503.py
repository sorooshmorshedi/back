# Generated by Django 2.0.5 on 2018-08-25 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sanads', '0022_auto_20180825_1434'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionitem',
            old_name='Cheque',
            new_name='cheque',
        ),
    ]
