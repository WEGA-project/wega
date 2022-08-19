# Generated by Django 4.1 on 2022-08-17 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0005_rename_mgno3_mo3_plantprofile_mgno3_no3'),
    ]

    operations = [
        migrations.AddField(
            model_name='plantprofile',
            name='calc_mode',
            field=models.CharField(choices=[('K', 'K2SO4'), ('Mg', 'MgNO3')], default='K', max_length=2),
        ),
    ]
