# Generated by Django 2.0.5 on 2019-04-10 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0018_auto_20190409_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='pricingType',
            field=models.IntegerField(choices=[(0, 'فایفو'), (1, 'میانگین موزون')]),
        ),
    ]