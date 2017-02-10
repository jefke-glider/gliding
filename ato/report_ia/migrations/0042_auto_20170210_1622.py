# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-10 16:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0041_auto_20170208_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='voorval',
            name='locatie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Vliegveld'),
        ),
        migrations.AlterField(
            model_name='startwijze',
            name='naam_kort',
            field=models.CharField(max_length=1),
        ),
    ]
