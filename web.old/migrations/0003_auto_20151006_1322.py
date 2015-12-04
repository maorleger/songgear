# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20151005_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='chords_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='chords_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='tabs_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='tabs_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='video',
            field=models.URLField(blank=True, null=True),
        ),
    ]
