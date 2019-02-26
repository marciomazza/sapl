# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-19 18:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import sapl.utils


class Migration(migrations.Migration):

    dependencies = [
        ('audiencia', '0009_remove_anexoaudienciapublica_indexacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anexoaudienciapublica',
            name='arquivo',
            field=models.FileField(default='Assunto não existente.', upload_to=sapl.utils.texto_upload_path, verbose_name='Arquivo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='anexoaudienciapublica',
            name='assunto',
            field=models.TextField(verbose_name='Assunto'),
        ),
        migrations.AlterField(
            model_name='anexoaudienciapublica',
            name='data',
            field=models.DateField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
