# Generated by Django 2.2 on 2020-07-21 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0003_auto_20200719_1719'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='factorexpense',
            options={'default_permissions': (), 'ordering': ['pk'], 'permissions': (('get.factorExpenses', 'مشاهده هزینه های فاکتور'), ('create.factorExpenses', 'تعریف هزینه های فاکتور'), ('update.factorExpenses', 'ویرایش هزینه های فاکتور'), ('delete.factorExpenses', 'حذف هزینه های فاکتور'), ('getOwn.factorExpenses', 'مشاهده هزینه های فاکتور خود'), ('updateOwn.factorExpenses', 'ویرایش هزینه های فاکتور خود'), ('deleteOwn.factorExpenses', 'حذف هزینه های فاکتور خود'))},
        ),
    ]
