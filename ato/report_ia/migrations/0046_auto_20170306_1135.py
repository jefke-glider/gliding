# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-06 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0045_auto_20170306_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voorval',
            name='ato',
            field=models.IntegerField(choices=[(1, 'ATO voorval'), (2, 'niet ATO voorval'), (3, 'onduidelijk (ATO/niet ATO)')], default=1),
        ),
    ]
