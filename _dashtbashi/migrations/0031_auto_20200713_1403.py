# Generated by Django 2.2 on 2020-07-13 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200708_1457'),
        ('_dashtbashi', '0030_auto_20200708_1141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='payableAccount',
        ),
        migrations.AddField(
            model_name='car',
            name='receivableAccount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='carReceivable', to='accounts.Account'),
        ),
    ]
