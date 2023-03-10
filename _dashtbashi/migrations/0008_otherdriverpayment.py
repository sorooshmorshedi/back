# Generated by Django 2.2 on 2020-07-26 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0005_auto_20200726_0940'),
        ('_dashtbashi', '0007_auto_20200726_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherDriverPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True)),
                ('updated_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True)),
                ('is_auto_created', models.BooleanField(default=False)),
                ('code', models.IntegerField()),
                ('date', django_jalali.db.models.jDateField()),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('driving', models.ManyToManyField(related_name='otherDriverPayments', to='_dashtbashi.Driving')),
                ('imprests', models.ManyToManyField(related_name='otherDriverPaymentsAsImprest', to='transactions.Transaction')),
                ('ladings', models.ManyToManyField(related_name='otherDriverPayment', to='_dashtbashi.Lading')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='otherDriverPayment', to='transactions.Transaction')),
            ],
            options={
                'ordering': ['pk'],
                'permissions': (('get.otherDriverPayment', 'مشاهده پرداخت رانندگان متفرقه '), ('create.otherDriverPayment', 'تعریف پرداخت رانندگان متفرقه'), ('update.otherDriverPayment', 'ویرایش پرداخت رانندگان متفرقه'), ('delete.otherDriverPayment', 'حذف پرداخت رانندگان متفرقه'), ('getOwn.otherDriverPayment', 'مشاهده پرداخت رانندگان متفرقه خود'), ('updateOwn.otherDriverPayment', 'ویرایش پرداخت رانندگان متفرقه خود'), ('deleteOwn.otherDriverPayment', 'حذف پرداخت رانندگان متفرقه خود')),
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]
