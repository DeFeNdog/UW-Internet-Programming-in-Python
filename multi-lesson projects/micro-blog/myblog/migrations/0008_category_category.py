# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-10 01:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0007_remove_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myblog.Post'),
        ),
    ]
