# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 16:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatefitbackend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=320)),
                ('address', models.TextField()),
                ('phone', models.TextField()),
                ('history', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=320)),
                ('description', models.TextField()),
                ('image', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Foods',
            },
        ),
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=320)),
                ('image', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=320)),
                ('description', models.TextField()),
                ('image', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MenuCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=320)),
                ('description', models.TextField()),
                ('image', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=320)),
                ('price', models.CharField(max_length=320)),
                ('order_date', models.DateTimeField(verbose_name='date published')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ultimatefitbackend.Customer')),
            ],
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.AddField(
            model_name='menu',
            name='menucategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ultimatefitbackend.MenuCategory'),
        ),
        migrations.AddField(
            model_name='food',
            name='foodcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ultimatefitbackend.FoodCategory'),
        ),
        migrations.AddField(
            model_name='food',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ultimatefitbackend.Menu'),
        ),
        migrations.AddField(
            model_name='food',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ultimatefitbackend.Order'),
        ),
    ]