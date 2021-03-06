# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 22:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Webtoon',
            fields=[
                ('toon_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('webtoon_title', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('thumbnail_url', models.URLField(null=True)),
                ('weekday', models.CharField(max_length=10)),
                ('lastest_no', models.IntegerField(null=True)),
                ('rating', models.FloatField(null=True)),
                ('uploaded_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('favorite', models.BooleanField(default=False)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webtoon_server.Site')),
            ],
            options={
                'ordering': ['webtoon_title'],
            },
        ),
        migrations.CreateModel(
            name='WebtoonEpisodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episode_title', models.CharField(max_length=50)),
                ('no', models.IntegerField()),
                ('uploaded_at', models.DateTimeField(default=datetime.datetime.now)),
                ('thumbnail_url', models.URLField(null=True)),
                ('rating', models.FloatField()),
                ('webtoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webtoon_server.Webtoon')),
            ],
            options={
                'get_latest_by': 'uploaded_at',
            },
        ),
        migrations.CreateModel(
            name='WebtoonEpisodeToon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField()),
                ('order', models.IntegerField()),
                ('webtoon_episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webtoon_server.WebtoonEpisodes')),
            ],
        ),
        migrations.CreateModel(
            name='WebtoonInit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initialized', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WebtoonThumbnail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=225)),
                ('url', models.CharField(max_length=225)),
                ('webtoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webtoon_server.Webtoon')),
            ],
        ),
    ]
