# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-04-09 13:44
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.models import Count
from django.db.models.functions import Lower


def remove_case_variations_of_oldusername_username(apps, schema_editor):
    OldUsername = apps.get_model('accounts', 'OldUsername')

    # Get all case-insensitive duplicate usernames which are used in more than one OldUsername object
    usernames = OldUsername.objects.values_list(Lower('username'), flat=True) \
        .annotate(num_username=Count('username')) \
        .filter(num_username__gt=1)

    # Iterate through them and leave only one OldUsername object per each username
    for username in usernames:
        OldUsername.objects.filter(
            id__in=OldUsername.objects.filter(username__iexact=username).values_list('id')[1:]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20201113_1132'),
    ]

    operations = [
        migrations.RunPython(remove_case_variations_of_oldusername_username, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='oldusername',
            name='username',
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
        migrations.RunSQL('CREATE UNIQUE INDEX "accounts_oldusername_username_upper_uniq" on "accounts_oldusername" (UPPER(username));')
    ]
