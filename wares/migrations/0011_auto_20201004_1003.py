# Generated by Django 2.2 on 2020-10-04 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0010_auto_20201001_1533'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='warelevel',
            unique_together=set(),
        ),
    ]
