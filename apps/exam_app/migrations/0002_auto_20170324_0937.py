# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 16:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userFavs', to='exam_app.User'),
        ),
    ]
