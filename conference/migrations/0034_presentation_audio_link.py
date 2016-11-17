# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-17 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0033_presentation_slide_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='audio_link',
            field=models.URLField(blank=True, help_text=b'The URL for an audio recording of the presentation.<br>If it can be embded then we will otherwise a link will be displayed', max_length=1024),
        ),
    ]