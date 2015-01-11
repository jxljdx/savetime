# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('savetimeapp', '0002_item_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 2, 6, 25, 48, 384023, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
