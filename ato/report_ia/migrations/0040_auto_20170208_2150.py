# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-08 21:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0039_auto_20170201_1014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voorval',
            name='muopo',
        ),
        migrations.AddField(
            model_name='voorval',
            name='mens',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='voorval',
            name='omgeving',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='voorval',
            name='organisatie',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='voorval',
            name='product',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='voorval',
            name='uitrusting',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='voorval',
            name='datum',
            field=models.DateField(),
        ),
    ]
