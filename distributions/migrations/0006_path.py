# Generated by Django 2.2 on 2021-02-26 10:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0018_auto_20210104_1053'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('distributions', '0005_auto_20210223_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Path',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True)),
                ('updated_at', django_jalali.db.models.jDateTimeField(blank=True, editable=False, null=True)),
                ('is_auto_created', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=150)),
                ('explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('level', models.IntegerField()),
                ('code', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='own_path', to=settings.AUTH_USER_MODEL)),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.FinancialYear')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='distributions.Path')),
                ('visitors', models.ManyToManyField(related_name='paths', to='distributions.Visitor')),
            ],
            options={
                'ordering': ['code'],
                'permissions': (('create.path0', 'تعریف '), ('get.ware', 'مشاهده کالا'), ('update.ware', 'ویرایش کالا'), ('delete.ware', 'حذف کالا'), ('getOwn.ware', 'مشاهده کالا های خود'), ('updateOwn.ware', 'ویرایش کالا های خود'), ('deleteOwn.ware', 'حذف کالا های خود'), ('sort.inventory', 'مرتب سازی کاردکس کالا')),
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]
