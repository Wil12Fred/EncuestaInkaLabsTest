# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-10-28 16:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('encuesta', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='alternativa_orden',
            unique_together=set([]),
        ),
    ]
