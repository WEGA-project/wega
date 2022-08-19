# Generated by Django 4.1 on 2022-08-15 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plantprofile',
            name='b',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='B'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='co',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='Co'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='cu',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='Cu'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='fe',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='Fe'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='mn',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='Mn'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='mo',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='Mo'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='si',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='Si'),
        ),
        migrations.AddField(
            model_name='plantprofile',
            name='zn',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='Zn'),
        ),
    ]