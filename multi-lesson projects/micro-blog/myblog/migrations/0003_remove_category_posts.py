# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-10 00:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_auto_20190210_0042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='posts',
        ),
    ]
