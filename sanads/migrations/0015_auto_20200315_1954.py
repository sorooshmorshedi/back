# Generated by Django 2.2 on 2020-03-15 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0016_financialyear_openingsanad'),
        ('sanads', '0014_auto_20200310_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sanad',
            name='code',
            field=models.IntegerField(verbose_name='شماره سند'),
        ),
        migrations.AlterUniqueTogether(
            name='sanad',
            unique_together={('code', 'financial_year')},
        ),
    ]