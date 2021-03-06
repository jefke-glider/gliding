# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 18:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0066_auto_20170410_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club_mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('voorval', models.BooleanField(default=False)),
                ('maatregel', models.BooleanField(default=False)),
                ('starts', models.BooleanField(default=False)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report_ia.Club')),
            ],
        ),
    ]
