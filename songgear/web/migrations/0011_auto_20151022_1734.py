# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20151016_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='lesson_video',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
    ]
