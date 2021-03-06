# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 10:48
from __future__ import unicode_literals

import conference.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text=b'Used to make a nice url for the page that displays this.')),
                ('name', models.CharField(max_length=1024)),
                ('biography', models.TextField(blank=True)),
                ('photo', models.ImageField(blank=True, upload_to=conference.models.person_photo_upload_to)),
                ('twitter_username', models.CharField(blank=True, max_length=15)),
                ('website', models.URLField(blank=True, max_length=1024)),
                ('facebook', models.URLField(blank=True, max_length=1024)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conference_attendee_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text=b'Used to make a nice url for the page that displays this.')),
                ('title', models.CharField(max_length=1024)),
                ('long_description', models.TextField()),
                ('short_description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=1024)),
                ('location', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text=b'Used to make a nice url for the page that displays this.')),
                ('name', models.CharField(max_length=1024)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, help_text=b'Only shown to admins, something to help you identify this slot in other forms.', max_length=1024)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('kind', models.CharField(choices=[(b'COFFEE', b'Coffee break'), (b'LUNCH', b'Lunch break'), (b'KEYNOTE', b'Keynote'), (b'WORKSHOP', b'Workshop'), (b'TALK', b'Talk')], max_length=100)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='slots', to='conference.Room')),
                ('schedule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='slots', to='conference.Schedule')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text=b'Used to make a nice url for the page that displays this.')),
                ('name', models.CharField(max_length=1024)),
                ('biography', models.TextField(blank=True)),
                ('photo', models.ImageField(blank=True, upload_to=conference.models.person_photo_upload_to)),
                ('twitter_username', models.CharField(blank=True, max_length=15)),
                ('website', models.URLField(blank=True, max_length=1024)),
                ('facebook', models.URLField(blank=True, max_length=1024)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conference_speaker_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='presentation',
            name='additional_speakers',
            field=models.ManyToManyField(related_name='additional_presentations', to='conference.Speaker'),
        ),
        migrations.AddField(
            model_name='presentation',
            name='primary_speaker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presentations', to='conference.Speaker'),
        ),
        migrations.AddField(
            model_name='presentation',
            name='slot',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='presentation', to='conference.Slot'),
        ),
    ]
