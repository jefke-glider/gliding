# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 14:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0057_auto_20170406_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voorval',
            name='thermiek',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Thermiek'),
        ),
        migrations.AlterField(
            model_name='voorval',
            name='windrichting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Windrichting'),
        ),
        migrations.AlterField(
            model_name='voorval',
            name='windsterkte',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Windsterkte'),
        ),
        migrations.AlterField(
            model_name='voorval',
            name='wolken',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Wolken'),
        ),
        migrations.AlterField(
            model_name='voorval',
            name='wolkenbasis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Wolkenbasis'),
        ),
        migrations.AlterField(
            model_name='voorval',
            name='zichtbaarheid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Zichtbaarheid'),
        ),
    ]