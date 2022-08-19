# Generated by Django 4.1 on 2022-08-16 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0003_alter_plantprofile_ca_alter_plantprofile_cl_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='micro',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='macro',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='micro',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='plant_profile',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='cacl2_ca',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='CaCl2_Ca'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='cacl2_cl',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='CaCl2_Cl'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='cano3_ca',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='CaNO3_Ca'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='cano3_nh4',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='CaNO3_NH4'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='cano3_no3',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='CaNO3_NO3'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='k2so4_k',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='K2SO4_K'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='k2so4_s',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='K2SO4_S'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='kh2po4_k',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='KH2PO4_K'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='kh2po4_p',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='KH2PO4_P'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='kno3_k',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='KNO3_K'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='kno3_no3',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='KNO3_NO3'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='mgno3_mg',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='MgNO3_Mg'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='mgno3_mo3',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='MgNO3_NO3'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='mgso4_mg',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='MgSO4_Mg'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='mgso4_s',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='MgSO4_S'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='nh4no3_nh4',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='NH4NO3_NH4'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='nh4no3_no3',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='NH4NO3_NO3'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='b',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='B'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='ca',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='Ca'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='cl',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='Cl'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='co',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='Co'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='cu',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='Cu'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='ec',
            field=models.DecimalField(decimal_places=3, max_digits=9, verbose_name='Ec'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='fe',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='Fe'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='k',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='K'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='mg',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='Mg'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='mn',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='Mn'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='mo',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='Mo'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='n',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='N'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='nh4',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='NH4'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='no3',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='NO3'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='p',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='P'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='ppm',
            field=models.DecimalField(decimal_places=3, max_digits=9, verbose_name='PPM'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='s',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='S'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='si',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='Si'),
        ),
        migrations.AlterField(
            model_name='plantprofile',
            name='zn',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='Zn'),
        ),
        migrations.DeleteModel(
            name='Macro',
        ),
        migrations.DeleteModel(
            name='Micro',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
