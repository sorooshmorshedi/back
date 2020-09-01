# Generated by Django 2.2 on 2020-09-01 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20200827_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='accounts', to='accounts.AccountType'),
            preserve_default=False,
        ),
    ]
