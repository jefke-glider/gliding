# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-18 16:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report_ia', '0028_auto_20170117_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nieuws',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bericht', models.TextField()),
                ('club', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('groep', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'verbose_name_plural': 'Berichten',
            },
        ),
    ]
