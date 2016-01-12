# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-24 11:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tv', '0005_auto_20151223_1743'),
    ]

    operations = [
        migrations.RenameField(
            model_name='credit',
            old_name='department_id',
            new_name='department',
        ),
        migrations.RenameField(
            model_name='credit',
            old_name='job_id',
            new_name='job',
        ),
        migrations.RenameField(
            model_name='credit',
            old_name='person_id',
            new_name='person',
        ),
        migrations.RenameField(
            model_name='credit',
            old_name='series_id',
            new_name='series',
        ),
        migrations.RenameField(
            model_name='episode',
            old_name='season_id',
            new_name='season',
        ),
        migrations.RenameField(
            model_name='episode',
            old_name='series_id',
            new_name='series',
        ),
        migrations.RenameField(
            model_name='job',
            old_name='department_id',
            new_name='department',
        ),
        migrations.RenameField(
            model_name='season',
            old_name='series_id',
            new_name='series',
        ),
    ]
