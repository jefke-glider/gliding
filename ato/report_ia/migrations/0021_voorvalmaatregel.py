# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-15 15:44
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0020_voorval_aantal_maatregelen'),
    ]

    operations = [        
        migrations.CreateModel(
            name='VoorvalMaatregel',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('datum', models.DateField()),
                ('uur', models.TimeField()),
                ('synopsis', models.TextField()),
                ('menselijke_schade', models.BooleanField(default=False)),
                ('materiele_schade', models.BooleanField(default=False)),
                ('schade_omschrijving', models.TextField()),
                ('muopo', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Mens'), (2, 'Uitrusting'), (3, 'Omgeving'), (4, 'Product'), (5, 'Organisatie')], max_length=3)),
                ('omschrijving', models.TextField()),
            ],
            options={
                'managed': False,
                'db_table': 'voorval_maatregel',
            },
        ),
        migrations.RunSQL(["""
 CREATE OR REPLACE VIEW voorval_maatregel AS 
 SELECT row_number() OVER () AS id,
    vv.datum,
    vv.uur,
    vv.type_voorval_id,
    vv.synopsis,
    vv.opleiding_id,
    vv.startwijze_id,
    vv.club_id,
    vv.menselijke_schade,
    vv.materiele_schade,
    vv.muopo,
    vv.type_toestel_id,
    vv.kern_activiteit_id,
    vv.schade_omschrijving,
    ma.omschrijving
   FROM report_ia_voorval vv
     LEFT JOIN report_ia_maatregel ma ON ma.voorval_id = vv.id;

ALTER TABLE voorval_maatregel
  OWNER TO ato_admin;
"""])
    ]