# Generated by Django 4.0.4 on 2022-05-20 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping_management', '0007_alter_oferta_url_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oferta',
            name='url_image',
            field=models.CharField(max_length=1000),
        ),
    ]