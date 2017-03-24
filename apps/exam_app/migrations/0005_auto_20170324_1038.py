# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0004_quote_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='quote',
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='user',
        ),
        migrations.AddField(
            model_name='quote',
            name='favorites',
            field=models.ManyToManyField(related_name='favQuote', to='exam_app.User'),
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]
