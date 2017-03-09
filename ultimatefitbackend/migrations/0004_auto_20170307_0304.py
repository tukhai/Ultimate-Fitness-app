# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatefitbackend', '0003_auto_20170306_0158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='food',
            name='day',
            field=models.CharField(default=1, max_length=320),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food',
            name='month',
            field=models.CharField(default=1, max_length=320),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food',
            name='year',
            field=models.CharField(default=1, max_length=320),
            preserve_default=False,
        ),
    ]