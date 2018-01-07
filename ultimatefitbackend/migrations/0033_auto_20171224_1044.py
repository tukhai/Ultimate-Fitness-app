# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-24 02:44
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatefitbackend', '0032_auto_20171129_2337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodtype',
            name='price',
        ),
        migrations.AddField(
            model_name='food',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('LE', 'Lean On Me'), ('MA', 'Maintain'), ('HE', 'Heavy Duty')], max_length=8),
        ),
        migrations.AddField(
            model_name='foodtype',
            name='price_heavy',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='foodtype',
            name='price_lean',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='foodtype',
            name='price_maintain',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]