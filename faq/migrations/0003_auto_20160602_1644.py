# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 15:44
from __future__ import unicode_literals

import autoslug.fields
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_auto_20160602_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqpage',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 6, 2, 15, 44, 19, 61541, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faqpage',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 6, 2, 15, 44, 20, 940932, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faqquestion',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 6, 2, 15, 44, 22, 716779, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faqquestion',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 6, 2, 15, 44, 24, 508861, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='faqpage',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, help_text=b'Used to make a nice url for this FAQ page.', populate_from=b'title', unique=True),
        ),
        migrations.AlterField(
            model_name='faqquestion',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, help_text=b'Used to make a nice name to link directly to this question.', populate_from=b'question', unique=True),
        ),
    ]