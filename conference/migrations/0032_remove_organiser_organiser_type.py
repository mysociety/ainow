# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-16 18:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0031_migrate_organisers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organiser',
            name='organiser_type',
        ),
    ]