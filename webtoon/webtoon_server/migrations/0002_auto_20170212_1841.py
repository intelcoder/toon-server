# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 23:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webtoon_server', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='webtoon',
            options={'ordering': ['title']},
        ),
        migrations.RenameField(
            model_name='webtoon',
            old_name='webtoon_title',
            new_name='title',
        ),
    ]
