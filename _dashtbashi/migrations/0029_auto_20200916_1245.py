# Generated by Django 2.2 on 2020-09-16 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('_dashtbashi', '0028_ladingbillnumber_revoked_at'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='driving',
            unique_together={('driver', 'car')},
        ),
    ]
