# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_song_lesson_video'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='song',
            unique_together=set([('artist', 'name')]),
        ),
    ]
