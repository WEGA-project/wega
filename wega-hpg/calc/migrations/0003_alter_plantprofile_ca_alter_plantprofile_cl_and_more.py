# Generated by Django 4.1 on 2022-08-16 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0002_plantprofile_b_plantprofile_co_plantprofile_cu_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantprofile',
            name='ca',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='Ca'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='cl',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='Cl'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='k',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='K'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='mg',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='Mg'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='n',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='N'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='nh4',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='NH4'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='no3',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='NO3'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='p',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='P'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='s',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='S'),
        ),
    ]
