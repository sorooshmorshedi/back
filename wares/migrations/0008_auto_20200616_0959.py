# Generated by Django 2.2 on 2020-06-16 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0007_auto_20200609_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ware',
            name='pricingType',
            field=models.CharField(choices=[('f', 'فایفو'), ('wm', 'میانگین موزون')], max_length=2),
        ),
    ]
