# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0069_auto_20170411_1038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='startwijze',
            options={'ordering': ['prio'], 'verbose_name_plural': 'Startwijzen'},
        ),
        migrations.AlterModelOptions(
            name='type_toestel',
            options={'ordering': ['naam'], 'verbose_name_plural': 'Type toestellen'},
        ),
        migrations.AddField(
            model_name='kern_activiteit',
            name='prio',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='startwijze',
            name='prio',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voorval',
            name='piste',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
