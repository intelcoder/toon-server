# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 04:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webtoon_server', '0004_webtoonepisodetoon_webtoon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webtoonepisodetoon',
            name='webtoon',
        ),
    ]