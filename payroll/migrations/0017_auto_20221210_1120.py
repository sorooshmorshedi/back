# Generated by Django 2.2 on 2022-12-10 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0016_auto_20221210_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='employee_status',
            field=models.IntegerField(blank=True, choices=[(1, 'عادی'), (2, 'جانباز'), (3, 'فرزند شهید'), (4, 'آزاده'), (5, 'نیروهای مسلح'), (6, 'سایر مشمولین بند14ماده91'), (7, ' قانون اجتناب از اخذ مالیات مضاعف اتباع خارجی مشمول')], null=True),
        ),
    ]
