# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 08:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0016_maatregelen'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Maatregelen',
            new_name='Maatregel',
        ),
    ]
