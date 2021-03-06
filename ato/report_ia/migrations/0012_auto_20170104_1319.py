# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-04 13:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0011_auto_20170104_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schade',
            name='materieel',
        ),
        migrations.RemoveField(
            model_name='schade',
            name='menselijk',
        ),
        migrations.AddField(
            model_name='voorval',
            name='kern_activiteit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Kern_activiteit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voorval',
            name='materieel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='voorval',
            name='menselijk',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='voorval',
            name='schade_omschrijving',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voorval',
            name='type_toestel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Type_toestel'),
            preserve_default=False,
        ),
    ]
