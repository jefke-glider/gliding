# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-23 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0073_auto_20171023_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='club_mail',
            name='funktie',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
