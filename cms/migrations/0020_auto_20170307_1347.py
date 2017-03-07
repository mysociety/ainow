# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-03-07 13:47
from __future__ import unicode_literals

import cms.blocks
from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0019_auto_20170307_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peoplepage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField([('heading', cms.blocks.HeadingBlock()), ('text', wagtail.wagtailcore.blocks.RichTextBlock()), ('people', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'name', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'position', wagtail.wagtailcore.blocks.CharBlock()), (b'organisation', wagtail.wagtailcore.blocks.CharBlock()), (b'bio', wagtail.wagtailcore.blocks.PageChooserBlock(required=False, target_model='cms.Person')), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock())]), icon='group', template='cms/blocks/people.html')), ('divider', cms.blocks.DividerBlock())], default=[]),
        ),
    ]
