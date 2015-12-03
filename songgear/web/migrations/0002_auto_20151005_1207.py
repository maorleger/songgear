# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='chords',
        ),
        migrations.RemoveField(
            model_name='song',
            name='tabs',
        ),
        migrations.AddField(
            model_name='song',
            name='chords_text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='chords_url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='tabs_text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='tabs_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='video',
            field=models.URLField(null=True),
        ),
        migrations.DeleteModel(
            name='External',
        ),
    ]
