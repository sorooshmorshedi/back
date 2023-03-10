# Generated by Django 2.2 on 2020-08-20 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sanads', '0008_auto_20200728_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sanad',
            name='createType',
            field=models.CharField(choices=[('auto', 'خودکار'), ('manual', 'دستی')], default='manual', max_length=20),
        ),
        migrations.AlterField(
            model_name='sanad',
            name='type',
            field=models.CharField(choices=[('temporary', 'موقت'), ('definite', 'قطعی')], default='temporary', max_length=20),
        ),
        migrations.AlterField(
            model_name='sanaditem',
            name='sanad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='sanads.Sanad', verbose_name='سند'),
        ),
    ]
