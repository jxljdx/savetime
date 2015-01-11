# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('savetimeapp', '0003_auto_20150102_0625'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='desc',
            field=models.CharField(default=datetime.datetime(2015, 1, 5, 0, 48, 11, 139881, tzinfo=utc), max_length=2048),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 5, 0, 47, 35, 478436, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
