# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-18 16:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0029_nieuws'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nieuws',
            old_name='club',
            new_name='user',
        ),
    ]
