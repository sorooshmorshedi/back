# Generated by Django 2.0.5 on 2018-09-12 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheques', '0002_auto_20180901_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cheque',
            name='status',
            field=models.CharField(choices=[('blank', 'blank'), ('notPassed', 'notPassed'), ('inFlow', 'inFlow'), ('passed', 'passed'), ('bounced', 'bounced'), ('cashed', 'cashed'), ('revoked', 'revoked'), ('transferred', 'transferred'), ('', 'any')], max_length=30),
        ),
        migrations.AlterField(
            model_name='statuschange',
            name='fromStatus',
            field=models.CharField(choices=[('blank', 'blank'), ('notPassed', 'notPassed'), ('inFlow', 'inFlow'), ('passed', 'passed'), ('bounced', 'bounced'), ('cashed', 'cashed'), ('revoked', 'revoked'), ('transferred', 'transferred'), ('', 'any')], max_length=30),
        ),
        migrations.AlterField(
            model_name='statuschange',
            name='toStatus',
            field=models.CharField(choices=[('blank', 'blank'), ('notPassed', 'notPassed'), ('inFlow', 'inFlow'), ('passed', 'passed'), ('bounced', 'bounced'), ('cashed', 'cashed'), ('revoked', 'revoked'), ('transferred', 'transferred'), ('', 'any')], max_length=30),
        ),
    ]
