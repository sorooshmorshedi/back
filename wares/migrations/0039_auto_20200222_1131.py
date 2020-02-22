# Generated by Django 2.2 on 2020-02-22 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0038_auto_20190720_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='pricingType',
            field=models.IntegerField(choices=[(0, 'فایفو'), (1, 'میانگین موزون')]),
        ),
        migrations.CreateModel(
            name='WareBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.DecimalField(decimal_places=6, max_digits=24)),
                ('ware', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='balance', to='wares.Ware')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='balance', to='wares.Warehouse')),
            ],
        ),
    ]
