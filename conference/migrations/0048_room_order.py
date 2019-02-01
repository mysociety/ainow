# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2019-02-01 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0047_presentation_prezi_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='order',
            field=models.IntegerField(help_text=b'Use to override the default (alphabetical) order of rooms.', null=True),
        ),
    ]
