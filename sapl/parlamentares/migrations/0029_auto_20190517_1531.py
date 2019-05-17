# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-17 18:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parlamentares', '0028_auto_20190515_1744'),
    ]

    operations = [
        migrations.RunSQL("""
            update base_autor
            set tipo_id = (select id
                           from base_tipoautor
                           where content_type_id = (select id
                                                    from django_content_type
                                                    where app_label = 'parlamentares' and model = 'bloco'))
            where tipo_id = (select id
		                     from base_tipoautor
		                     where content_type_id = (select id
					         from django_content_type
					         where app_label = 'sessao' and model = 'bloco'));
        """),
        migrations.RunSQL("""
            delete from base_tipoautor
            where content_type_id = (select id
                                     from django_content_type
                                     where app_label = 'sessao' and model = 'bloco')
        """)
    ]
