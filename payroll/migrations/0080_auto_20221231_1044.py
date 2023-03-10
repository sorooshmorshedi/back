# Generated by Django 2.2 on 2022-12-31 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0079_auto_20221231_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hrletter',
            name='ayabo_zahab_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='bon_kharo_bar_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='fogholade_badi_abohava_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='fogholade_mahal_khedmat_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='fogholade_sakhti_kar_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='fogholade_sharayet_mohit_kar_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='fogholade_shoghl_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='haghe_ankal_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='haghe_jazb_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='haghe_maskan_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='haghe_modiriyat_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='haghe_sarparasti_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='haghe_shir_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='haghe_taahol_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='haghe_tahsilat_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='hoghooghe_roozane_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='komakhazine_mahdekoodak_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='komakhazine_mobile_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='komakhazine_varzesh_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='mahroomiat_tashilat_zendegi_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='mazaya_mostamar_gheyre_naghdi_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='paye_sanavat_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='hrletter',
            name='yarane_ghaza_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=24, null=True),
        ),
    ]
