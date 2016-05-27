# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentation',
            name='additional_speakers',
            field=models.ManyToManyField(blank=True, related_name='additional_presentations', to='conference.Speaker'),
        ),
    ]
