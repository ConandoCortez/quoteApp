# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0003_auto_20170324_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='author',
            field=models.CharField(default='Conan', max_length=255),
            preserve_default=False,
        ),
    ]