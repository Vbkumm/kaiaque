# Generated by Django 2.2 on 2019-11-22 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_auto_20191120_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiencemodel',
            name='experience_equipment',
            field=models.BooleanField(choices=[(None, ''), (True, 'Sim'), (False, 'Não')], default=None, max_length=3, verbose_name='Precisa de algum equipamento?'),
        ),
    ]
