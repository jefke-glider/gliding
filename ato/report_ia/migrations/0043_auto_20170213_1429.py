# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-13 14:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0042_auto_20170210_1622'),
    ]

    operations = [
                migrations.RunSQL(["""
TRUNCATE report_ia_ato_gebruiker CASCADE;                
TRUNCATE report_ia_vliegveld CASCADE;
TRUNCATE report_ia_club CASCADE;
ALTER SEQUENCE report_ia_vliegveld_id_seq RESTART WITH 1;
ALTER SEQUENCE report_ia_club_id_seq RESTART WITH 1;
COPY report_ia_vliegveld (naam, afkorting_icao ) FROM '/home/jpe/proj/ato/ato/db/vliegvelden.csv' WITH (FORMAT CSV, ENCODING UTF8);
COPY report_ia_club (naam, naam_kort, locatie_id ) FROM '/home/jpe/proj/ato/ato/db/clubs.csv' WITH (FORMAT CSV, ENCODING UTF8);
"""]),
    ]