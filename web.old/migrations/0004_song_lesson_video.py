# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20151006_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='lesson_video',
            field=models.URLField(blank=True, null=True),
        ),
    ]
