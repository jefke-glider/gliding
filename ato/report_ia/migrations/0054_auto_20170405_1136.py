# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0053_auto_20170329_1235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aantalstarts',
            name='op_datum',
        ),
        migrations.AddField(
            model_name='aantalstarts',
            name='ingevuld_op',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='aantalstarts',
            name='tot',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='aantalstarts',
            name='van',
            field=models.DateField(blank=True, null=True),
        ),
    ]
