# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-13 16:54
from __future__ import unicode_literals

from django.db import migrations

from ..utilities import create_ato_users

class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0043_auto_20170213_1429'),
    ]

    operations = [
        migrations.RunPython(create_ato_users)
    ]
