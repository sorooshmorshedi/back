# Generated by Django 2.2 on 2021-01-23 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0019_auto_20210121_1348'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='saleprice',
            unique_together={('ware', 'unit')},
        ),
    ]