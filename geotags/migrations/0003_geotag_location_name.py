# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-01-11 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geotags', '0002_auto_20220111_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='geotag',
            name='location_name',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
