# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 12:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_ia', '0014_kern_gevaar_potentieel_risico'),
    ]

    operations = [
        migrations.RunSQL([
            "insert into report_ia_kern_gevaar (naam) values ('onzorgvuldige/geen cockpitcheck');",
            "insert into report_ia_kern_gevaar (naam) values ('onzorgvuldige/geen daily check');",
            "insert into report_ia_kern_gevaar (naam) values ('circuleren op operationeel terrein');",
            "insert into report_ia_kern_gevaar (naam) values ('gebrekkig onderhoud LVT');",
            "insert into report_ia_kern_gevaar (naam) values ('staat van de infrastructuur');",
            "insert into report_ia_kern_gevaar (naam) values ('gebrek aan toezicht door bevoegde persoon');",
            "insert into report_ia_kern_gevaar (naam) values ('onervarenheid piloot in');",
            "insert into report_ia_kern_gevaar (naam) values ('onzorgvuldige aankoppelprocedure lier');",
            "insert into report_ia_kern_gevaar (naam) values ('onzorgvuldige aankoppelprocedure sleper');",
            "insert into report_ia_kern_gevaar (naam) values ('luchtruim');",
            ]
            )

    ]
