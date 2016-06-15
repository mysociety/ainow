# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-09 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0008_attendee_schedule'),
        ('pages', '0002_page_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='schedule',
        ),
        migrations.AddField(
            model_name='page',
            name='schedules',
            field=models.ManyToManyField(blank=True, help_text=b"Which schedules is this related to? If a schedule is private, this page will be kept private too, but only when viewing it in that context.<br> You probably only want to select multiple schedules if this is a public page that's shared between all schedules (like the privacy page).<br>You can't set this individually on child pages, set it once on the top level page and it will be applied to all the children automatically.", null=True, to='conference.Schedule'),
        ),
    ]