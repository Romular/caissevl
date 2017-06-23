# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caisse', '0002_auto_20170613_1705'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['ordre']},
        ),
        migrations.AlterModelOptions(
            name='categorie',
            options={'ordering': ['nom']},
        ),
        migrations.RemoveField(
            model_name='article',
            name='quantite_vente',
        ),
        migrations.AddField(
            model_name='lignecommande',
            name='prix_vente',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='prix_vente',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='commande',
            name='montant_total',
            field=models.FloatField(default=0),
        ),
    ]