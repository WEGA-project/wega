# Generated by Django 4.1 on 2022-09-14 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('wiki', '0002_wiki_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wiki',
            name='main_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image'),
        ),
    ]
