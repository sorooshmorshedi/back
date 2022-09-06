# Generated by Django 2.2 on 2022-09-04 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0017_listofpayitem_total_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hrletter',
            name='ayabo_zahab_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='bon_kharo_bar_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='fogholade_badi_abohava_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='fogholade_mahal_khedmat_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='fogholade_sakhti_kar_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='fogholade_sharayet_mohit_kar_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='haghe_ankal_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='haghe_maskan_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='haghe_shir_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='haghe_taahol_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='haghe_tahsilat_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='komakhazine_mahdekoodak_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='komakhazine_mobile_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='komakhazine_varzesh_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='mahroomiat_tashilat_zendegi_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='yarane_ghaza_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='listofpayitem',
            name='ezafe_kari',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='listofpayitem',
            name='kasre_kar',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='listofpayitem',
            name='shab_kari',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='listofpayitem',
            name='tatil_kari',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=24),
        ),
    ]
