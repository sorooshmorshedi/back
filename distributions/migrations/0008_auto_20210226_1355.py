# Generated by Django 2.2 on 2021-02-26 10:25

from django.db import migrations, models
import helpers.db


class Migration(migrations.Migration):

    dependencies = [
        ('distributions', '0007_auto_20210226_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='path',
            name='visitors',
            field=models.ManyToManyField(blank=True, default=helpers.db.get_empty_array, related_name='paths', to='distributions.Visitor'),
        ),
    ]