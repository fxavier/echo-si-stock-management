# Generated by Django 3.2.13 on 2022-08-01 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumo',
            name='id_requisicao',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
