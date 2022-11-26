# Generated by Django 2.2 on 2021-12-28 08:25

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('contracting', '0002_auto_20211227_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='contractor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contract', to='accounts.Account'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='from_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='submit_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='tender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contract', to='contracting.Tender'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='to_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='transAction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contract', to='transactions.Transaction'),
        ),
        migrations.AlterField(
            model_name='tender',
            name='offer_expiration',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tender',
            name='opening_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tender',
            name='received_deadline',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tender',
            name='send_offer_deadline',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tender',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tender', to='transactions.Transaction'),
        ),
    ]