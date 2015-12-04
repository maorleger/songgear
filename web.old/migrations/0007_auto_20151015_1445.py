# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0006_auto_20151011_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('create_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='song',
            old_name='created',
            new_name='create_date',
        ),
        migrations.RenameField(
            model_name='song',
            old_name='updated',
            new_name='update_date',
        ),
        migrations.AddField(
            model_name='comment',
            name='song',
            field=models.ForeignKey(to='web.Song'),
        ),
    ]
