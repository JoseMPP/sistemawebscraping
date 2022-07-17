# Generated by Django 4.0.4 on 2022-05-11 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ejecucion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping_management.categoria')),
            ],
        ),
        migrations.RenameField(
            model_name='spider',
            old_name='esProduccion',
            new_name='es_produccion',
        ),
        migrations.AlterField(
            model_name='caracteristica',
            name='nombre',
            field=models.CharField(max_length=30),
        ),
        migrations.CreateModel(
            name='EjecucionParametro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_parametro', models.CharField(max_length=100)),
                ('ejecucion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping_management.ejecucion')),
                ('parametro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping_management.parametro')),
            ],
        ),
        migrations.AddField(
            model_name='ejecucion',
            name='parametros',
            field=models.ManyToManyField(through='scraping_management.EjecucionParametro', to='scraping_management.parametro'),
        ),
        migrations.AddField(
            model_name='ejecucion',
            name='spider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping_management.spider'),
        ),
    ]
