# Generated by Django 2.2 on 2020-10-15 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0011_auto_20201004_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='ware',
            name='level',
            field=models.IntegerField(choices=[(0, 'nature'), (1, 'group'), (2, 'category'), (3, 'ware')], default=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ware',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='wares.Ware'),
        ),
        migrations.AlterField(
            model_name='ware',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='wares', to='wares.WareLevel'),
        ),
        migrations.AlterField(
            model_name='ware',
            name='pricingType',
            field=models.CharField(blank=True, choices=[('f', 'فایفو'), ('wm', 'میانگین موزون')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='ware',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='wares', to='wares.Unit'),
        ),
        migrations.AlterField(
            model_name='ware',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='wares', to='wares.Warehouse'),
        ),
    ]
