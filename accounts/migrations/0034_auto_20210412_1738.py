# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-04-12 17:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_auto_20210412_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdeletionrequest',
            name='email_from',
            field=models.CharField(help_text=b'The email from which the user deletion requestwas received.', max_length=200),
        ),
        migrations.AlterField(
            model_name='userdeletionrequest',
            name='user_to',
            field=models.ForeignKey(help_text=b'The user account that should be deleted if this request proceeds. Note that you can click on the magnifying glass icon and search by email.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deletion_requests_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
