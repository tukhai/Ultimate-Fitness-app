# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-09-30 13:29
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatefitbackend', '0051_auto_20180930_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponpromotion',
            name='absolute_with_min',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='couponpromotion',
            name='cap_percentage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='couponpromotion',
            name='min_absolute',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='couponpromotion',
            name='percentage_with_cap',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
