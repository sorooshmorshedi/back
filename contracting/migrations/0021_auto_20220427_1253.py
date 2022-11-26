# Generated by Django 2.2 on 2022-04-27 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0028_auto_20210918_1233'),
        ('contracting', '0020_auto_20220425_1041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='guarantee_document_transaction',
        ),
        migrations.AddField(
            model_name='contract',
            name='guarantee_document_transaction',
            field=models.ManyToManyField(blank=True, null=True, related_name='contract_guarantee', to='transactions.Transaction'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='received_transaction',
            field=models.ManyToManyField(blank=True, null=True, related_name='contract_received', to='transactions.Transaction'),
        ),
        migrations.RemoveField(
            model_name='tender',
            name='transaction',
        ),
        migrations.AddField(
            model_name='tender',
            name='transaction',
            field=models.ManyToManyField(blank=True, null=True, related_name='tender', to='transactions.Transaction'),
        ),
    ]