# Generated by Django 2.2 on 2022-09-04 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0012_listofpayitem_mission_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='mission_pay_nerkh',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=24),
        ),
        migrations.AddField(
            model_name='workshop',
            name='mission_pay_type',
            field=models.CharField(choices=[('d', 'حداقل حقوق روزانه'), ('b', 'مزد مبنا')], default='b', max_length=1),
        ),
        migrations.AlterField(
            model_name='listofpayitem',
            name='sanavat_base',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
    ]
