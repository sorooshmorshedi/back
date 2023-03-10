# Generated by Django 2.2 on 2020-11-07 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wares', '0013_auto_20201017_1051'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='unit',
            options={'default_permissions': (), 'ordering': ['-pk'], 'permissions': (('get.unit', 'مشاهده واحد'), ('create.unit', 'تعریف واحد'), ('update.unit', 'ویرایش واحد'), ('delete.unit', 'حذف واحد'), ('getOwn.unit', 'مشاهده واحد های خود'), ('updateOwn.unit', 'ویرایش واحد های خود'), ('deleteOwn.unit', 'حذف واحد های خود'))},
        ),
        migrations.AlterModelOptions(
            name='warehouse',
            options={'default_permissions': (), 'ordering': ['-pk'], 'permissions': (('get.warehouse', 'مشاهده انبار'), ('create.warehouse', 'تعریف انبار'), ('update.warehouse', 'ویرایش انبار'), ('delete.warehouse', 'حذف انبار'), ('getOwn.warehouse', 'مشاهده انبار های خود'), ('updateOwn.warehouse', 'ویرایش انبار های خود'), ('deleteOwn.warehouse', 'حذف انبار های خود'))},
        ),
    ]
