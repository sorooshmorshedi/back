# Generated by Django 2.2 on 2021-06-01 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20210502_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultaccount',
            name='account_level',
            field=models.CharField(choices=[(0, 'group'), (1, 'kol'), (2, 'moein'), (3, 'tafsili')], default=3, max_length=1),
        ),
    ]
