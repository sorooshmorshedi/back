# Generated by Django 2.2 on 2020-03-02 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanads', '0008_auto_20200225_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionitem',
            name='bankName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='transactionitem',
            name='documentNumber',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='transactionitem',
            name='explanation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]