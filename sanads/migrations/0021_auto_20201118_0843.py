# Generated by Django 2.2 on 2020-11-18 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sanads', '0020_sanaditem_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sanaditem',
            options={'default_permissions': (), 'ordering': ('-order', 'pk'), 'permissions': ()},
        ),
    ]