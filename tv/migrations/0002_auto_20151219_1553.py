# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-19 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tv', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='episode_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='season',
            name='series_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tv.Series'),
            preserve_default=False,
        ),
    ]