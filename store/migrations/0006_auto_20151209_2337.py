# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 05:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20151209_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='oss_object',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='products',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 9, 23, 37, 6, 724554)),
        ),
    ]
