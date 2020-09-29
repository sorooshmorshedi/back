# Generated by Django 2.2 on 2020-09-29 10:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20200920_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='نام کاربری باید از حدوف و اعداد انگلیسی تشکیل شود', regex='^[a-zA-Z0-9]+$')]),
        ),
    ]