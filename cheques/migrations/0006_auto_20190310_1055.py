# Generated by Django 2.0.5 on 2019-03-10 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheques', '0005_auto_20190305_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cheque',
            name='type',
            field=models.CharField(choices=[('p', 'شخصی'), ('op', 'شخصی سایرین'), ('c', 'شرکت'), ('oc', 'شرکت سایرین')], max_length=1),
        ),
    ]
