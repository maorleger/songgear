# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_auto_20151022_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
