# Generated by Django 2.2 on 2022-04-25 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0028_auto_20210918_1233'),
        ('contracting', '0019_auto_20220418_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='guarantee_document_transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contract', to='transactions.Transaction'),
        ),
        migrations.RemoveField(
            model_name='contract',
            name='received_transaction',
        ),
        migrations.AddField(
            model_name='contract',
            name='received_transaction',
            field=models.ManyToManyField(related_name='contract_received', to='transactions.Transaction'),
        ),
    ]
