# Generated by Django 2.2 on 2019-11-08 22:14

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Board',
        ),
        migrations.AlterField(
            model_name='experiencemeetpointmodel',
            name='e_address',
            field=models.CharField(max_length=100, verbose_name='Qual o endereço do ponto de encontro para inicio da experiência?'),
        ),
        migrations.AlterField(
            model_name='experiencemeetpointmodel',
            name='e_city',
            field=models.CharField(max_length=50, verbose_name='Qual a cidade?'),
        ),
        migrations.AlterField(
            model_name='experiencemeetpointmodel',
            name='e_location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Indique a localização geografica no mapa'),
        ),
    ]
