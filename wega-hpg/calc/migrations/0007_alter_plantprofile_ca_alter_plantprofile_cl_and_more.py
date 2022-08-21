# Generated by Django 4.1 on 2022-08-20 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0006_plantprofile_calc_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantprofile',
            name='ca',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=9, verbose_name='Ca'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='cl',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=9, verbose_name='Cl'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='k',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=9, verbose_name='K'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='mg',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=9, verbose_name='Mg'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='n',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=9, verbose_name='N'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='nh4',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=9, verbose_name='NH4'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='no3',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=9, verbose_name='NO3'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='p',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=9, verbose_name='P'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='s',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=9, verbose_name='S'),
        ),
    ]