# Generated by Django 2.2 on 2020-07-23 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheques', '0005_auto_20200721_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cheque',
            name='type',
            field=models.CharField(blank=True, choices=[('p', 'شخصی'), ('op', 'شخصی سایرین'), ('c', 'شرکت'), ('oc', 'شرکت سایرین')], max_length=2),
        ),
    ]