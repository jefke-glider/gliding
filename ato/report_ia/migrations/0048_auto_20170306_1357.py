# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-06 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0047_auto_20170306_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='voorval',
            name='andere_locatie',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='voorval',
            name='schade_omschrijving',
            field=models.TextField(null=True),
        ),
    ]