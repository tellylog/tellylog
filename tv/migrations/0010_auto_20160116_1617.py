# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-16 15:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tv', '0009_auto_20160113_1601'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='episode',
            options={'ordering': ['number'], 'verbose_name': 'Episode', 'verbose_name_plural': 'Episodes'},
        ),
    ]
