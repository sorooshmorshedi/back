# Generated by Django 2.2 on 2022-12-15 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0037_auto_20221215_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adjustment',
            name='defined_by',
        ),
        migrations.RemoveField(
            model_name='adjustment',
            name='definition_date',
        ),
        migrations.RemoveField(
            model_name='adjustment',
            name='is_defined',
        ),
        migrations.RemoveField(
            model_name='adjustment',
            name='is_locked',
        ),
        migrations.RemoveField(
            model_name='adjustment',
            name='lock_date',
        ),
        migrations.RemoveField(
            model_name='adjustment',
            name='locked_by',
        ),
        migrations.RemoveField(
            model_name='contractrow',
            name='defined_by',
        ),
        migrations.RemoveField(
            model_name='contractrow',
            name='definition_date',
        ),
        migrations.RemoveField(
            model_name='contractrow',
            name='is_defined',
        ),
        migrations.RemoveField(
            model_name='contractrow',
            name='is_locked',
        ),
        migrations.RemoveField(
            model_name='contractrow',
            name='lock_date',
        ),
        migrations.RemoveField(
            model_name='contractrow',
            name='locked_by',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='defined_by',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='definition_date',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='is_defined',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='is_locked',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='lock_date',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='locked_by',
        ),
        migrations.RemoveField(
            model_name='personnelfamily',
            name='defined_by',
        ),
        migrations.RemoveField(
            model_name='personnelfamily',
            name='definition_date',
        ),
        migrations.RemoveField(
            model_name='personnelfamily',
            name='is_defined',
        ),
        migrations.RemoveField(
            model_name='personnelfamily',
            name='is_locked',
        ),
        migrations.RemoveField(
            model_name='personnelfamily',
            name='lock_date',
        ),
        migrations.RemoveField(
            model_name='personnelfamily',
            name='locked_by',
        ),
        migrations.RemoveField(
            model_name='workshop',
            name='defined_by',
        ),
        migrations.RemoveField(
            model_name='workshop',
            name='definition_date',
        ),
        migrations.RemoveField(
            model_name='workshop',
            name='is_defined',
        ),
        migrations.RemoveField(
            model_name='workshop',
            name='is_locked',
        ),
        migrations.RemoveField(
            model_name='workshop',
            name='lock_date',
        ),
        migrations.RemoveField(
            model_name='workshop',
            name='locked_by',
        ),
        migrations.RemoveField(
            model_name='workshoppersonnel',
            name='defined_by',
        ),
        migrations.RemoveField(
            model_name='workshoppersonnel',
            name='definition_date',
        ),
        migrations.RemoveField(
            model_name='workshoppersonnel',
            name='is_defined',
        ),
        migrations.RemoveField(
            model_name='workshoppersonnel',
            name='is_locked',
        ),
        migrations.RemoveField(
            model_name='workshoppersonnel',
            name='lock_date',
        ),
        migrations.RemoveField(
            model_name='workshoppersonnel',
            name='locked_by',
        ),
        migrations.RemoveField(
            model_name='workshoptax',
            name='defined_by',
        ),
        migrations.RemoveField(
            model_name='workshoptax',
            name='definition_date',
        ),
        migrations.RemoveField(
            model_name='workshoptax',
            name='is_defined',
        ),
        migrations.RemoveField(
            model_name='workshoptax',
            name='is_locked',
        ),
        migrations.RemoveField(
            model_name='workshoptax',
            name='lock_date',
        ),
        migrations.RemoveField(
            model_name='workshoptax',
            name='locked_by',
        ),
    ]