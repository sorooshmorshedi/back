# Generated by Django 2.2 on 2021-03-16 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20210301_1140'),
        ('distributions', '0017_visitor_defaultaccounts'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='distributor',
            options={'default_permissions': (), 'get_latest_by': 'pk', 'ordering': ['-pk'], 'permissions': (('create.distributor', 'تعریف موزع'), ('get.distributor', 'مشاهده موزع ها'), ('update.distributor', 'ویرایش موزع'), ('delete.distributor', 'حذف موزع'), ('getOwn.distributor', 'مشاهده موزع های خود'), ('updateOwn.distributor', 'ویرایش موزع های خود'), ('deleteOwn.distributor', 'حذف موزع های خود'))},
        ),
        migrations.AddField(
            model_name='distributor',
            name='defaultAccounts',
            field=models.ManyToManyField(related_name='distributors', to='accounts.DefaultAccount'),
        ),
    ]