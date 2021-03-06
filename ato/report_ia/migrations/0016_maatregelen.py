# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 08:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0015_auto_20170111_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maatregelen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingave', models.DateTimeField(auto_now=True)),
                ('omschrijving', models.TextField()),
                ('voorval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report_ia.Voorval')),
            ],
            options={
                'verbose_name_plural': 'Maatregelen',
            },
        ),
    ]
