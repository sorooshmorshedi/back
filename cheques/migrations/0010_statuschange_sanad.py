# Generated by Django 2.0.5 on 2018-08-16 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sanads', '0016_auto_20180814_1403'),
        ('cheques', '0009_auto_20180816_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='statuschange',
            name='sanad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='statusChange', to='sanads.Sanad'),
            preserve_default=False,
        ),
    ]
