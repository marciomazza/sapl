# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-29 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocoloadm', '0018_auto_20190314_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='tramitacaoadministrativo',
            name='urgente',
            field=models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=False, verbose_name='Urgente ?'),
        ),
        migrations.AlterField(
            model_name='tramitacaoadministrativo',
            name='texto',
            field=models.TextField(verbose_name='Texto da Ação'),
        ),
    ]
