# Generated by Django 2.2 on 2022-12-10 07:45

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0015_workshoppersonnel_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshoppersonnel',
            name='work_title_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='contract_type',
            field=models.IntegerField(blank=True, choices=[(2, 'پاره وقت'), (1, 'تمام وقت'), (3, 'موقت'), (5, 'ساعتی'), (4, 'پیمانی')], null=True),
        ),
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='employee_status',
            field=models.IntegerField(blank=True, choices=[(1, 'عادی'), (2, 'جانباز'), (3, 'فرزند شهید'), (4, 'آزاده'), (5, 'نیروهای مسلح'), (6, 'سایر مشمولین بند14ماده11'), (7, ' قانون اجتناب از اخذ مالیات مضاعف اتباع خارجی مشمول')], null=True),
        ),
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='employment_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='employment_type',
            field=models.IntegerField(blank=True, choices=[(4, 'پیمانی'), (1, 'قراردادی'), (2, 'َشرکتی'), (5, 'مامور'), (3, 'رسمی'), (6, 'سایر')], null=True),
        ),
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='job_group',
            field=models.IntegerField(blank=True, choices=[(2, 'آموزشي و فرهنگي'), (1, 'اداري و مالي'), (3, 'اموراجتماعي'), (5, 'درماني و بهداشتي'), (4, 'اطلاعات فناوري'), (7, 'خدمات'), (6, 'فني و مهندسي'), (8, 'كشاورزي ومحيط زيست'), (13, 'تولیدی'), (15, 'تحقیقاتی'), (11, 'کارگری'), (10, 'حراست و نگهبانی'), (12, 'ترابری'), (9, 'بازاریابی و فروش'), (17, 'قضات'), (16, 'انبارداری'), (14, 'کنترل کیفی'), (18, 'هیات علمی'), (0, 'سایر')], null=True),
        ),
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='job_location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='job_location_status',
            field=models.IntegerField(blank=True, choices=[(1, 'معمولی'), (2, 'مناطق کمتر توسعه یافته'), (3, 'مناطق آزاد تجاری')], null=True),
        ),
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='job_position',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='previous_insurance_history_in_workshop',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='previous_insurance_history_out_workshop',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workshoppersonnel',
            name='work_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]