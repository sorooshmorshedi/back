# Generated by Django 2.2 on 2020-08-09 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sanads', '0008_auto_20200728_1309'),
        ('_dashtbashi', '0017_auto_20200809_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='lading',
            name='contractor_type',
            field=models.CharField(choices=[('cmp', 'شرکت'), ('o', 'دیگر')], default='o', max_length=3),
        ),
        migrations.AddField(
            model_name='lading',
            name='sanad',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ladings', to='sanads.Sanad'),
        ),
        migrations.AddField(
            model_name='lading',
            name='ware_type',
            field=models.CharField(choices=[('b', 'خریداری شده'), ('s', 'فروش رفتخ')], max_length=2, null=True),
        ),
    ]