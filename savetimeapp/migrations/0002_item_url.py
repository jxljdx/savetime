# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('savetimeapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='url',
            field=models.CharField(default=datetime.datetime(2015, 1, 2, 6, 12, 0, 770578, tzinfo=utc), max_length=300),
            preserve_default=False,
        ),
    ]
