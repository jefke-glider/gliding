# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-28 09:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0050_auto_20170310_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thermiek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sterkte', models.CharField(max_length=3)),
                ('omschrijving', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Thermiek-sterktes',
            },
        ),
        migrations.CreateModel(
            name='Windrichting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uit', models.CharField(max_length=3)),
            ],
            options={
                'verbose_name_plural': 'Wind richtingen',
            },
        ),
        migrations.CreateModel(
            name='Windsterkte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kts', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Wind sterktes',
            },
        ),
        migrations.CreateModel(
            name='Wolken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('okta', models.CharField(max_length=5)),
                ('metar_code', models.CharField(max_length=3)),
                ('omschrijving', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Wolken',
            },
        ),
        migrations.CreateModel(
            name='Wolkenbasis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feet', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name_plural': 'Wolkenbasissen',
            },
        ),
        migrations.CreateModel(
            name='Zichtbaarheid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('km', models.CharField(max_length=5)),
                ('omschrijving', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Zichtbaarheden',
            },
        ),
        migrations.AddField(
            model_name='voorval',
            name='thermiek',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Thermiek'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voorval',
            name='windrichting',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Windrichting'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voorval',
            name='windsterkte',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Windsterkte'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voorval',
            name='wolken',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Wolken'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voorval',
            name='wolkenbasis',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Wolkenbasis'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voorval',
            name='zichtbaarheid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='report_ia.Zichtbaarheid'),
            preserve_default=False,
        ),
                migrations.RunSQL(["""
                insert into report_ia_windsterkte (kts) values ('0.5');
                insert into report_ia_windsterkte (kts) values ('6-15');
                insert into report_ia_windsterkte (kts) values ('16-25');
                insert into report_ia_windsterkte (kts) values ('> 25');
                
                insert into report_ia_windrichting (uit) values ('N');
                insert into report_ia_windrichting (uit) values ('NO');
                insert into report_ia_windrichting (uit) values ('O');
                insert into report_ia_windrichting (uit) values ('ZO');
                insert into report_ia_windrichting (uit) values ('Z');
                insert into report_ia_windrichting (uit) values ('ZW');
                insert into report_ia_windrichting (uit) values ('W');
                insert into report_ia_windrichting (uit) values ('NW');
                
                insert into report_ia_wolken (okta, metar_code, omschrijving ) values ('0', 'SKC', 'sky clear');
                insert into report_ia_wolken (okta, metar_code, omschrijving ) values ('1-2', 'FEW', 'few');
                insert into report_ia_wolken (okta, metar_code, omschrijving ) values ('3-4', 'SCT', 'scattered');
                insert into report_ia_wolken (okta, metar_code, omschrijving ) values ('5-7', 'BKN', 'broken');
                insert into report_ia_wolken (okta, metar_code, omschrijving ) values ('8', 'OVC', 'overcast');
                insert into report_ia_thermiek (sterkte, omschrijving ) values ('<1', 'zwak');
                insert into report_ia_thermiek (sterkte, omschrijving ) values ('1-3', 'matig');
                insert into report_ia_thermiek (sterkte, omschrijving ) values ('3-5', 'vrij krachtig');
                insert into report_ia_thermiek (sterkte, omschrijving ) values ('>5', 'krachtig');
                
                
                insert into report_ia_wolkenbasis (feet) values ('300-500');
                insert into report_ia_wolkenbasis (feet) values ('600-900');
                insert into report_ia_wolkenbasis (feet) values ('1000-2000');
                insert into report_ia_wolkenbasis (feet) values ('>3000');

                insert into report_ia_zichtbaarheid ( km, omschrijving) values ('<3', 'ondermaats');
                insert into report_ia_zichtbaarheid ( km, omschrijving) values ('3-4', 'slecht');
                insert into report_ia_zichtbaarheid ( km, omschrijving) values ('5-7', 'matig');
                insert into report_ia_zichtbaarheid ( km, omschrijving) values ('8-10', 'goed');
               insert into report_ia_zichtbaarheid ( km, omschrijving) values ('> 10', 'uitstekend');
                                
"""]),
    ]