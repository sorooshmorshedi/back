# Generated by Django 2.2 on 2020-07-26 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imprests', '0006_auto_20200726_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imprestsettlement',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='imprestSettlement', to='transactions.Transaction'),
        ),
    ]