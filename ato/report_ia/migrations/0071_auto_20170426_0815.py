# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 08:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0070_auto_20170426_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kern_activiteit',
            name='prio',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='startwijze',
            name='prio',
            field=models.IntegerField(),
        ),
    ]