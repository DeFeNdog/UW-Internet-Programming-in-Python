# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-10 02:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0012_auto_20190210_0158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='post',
        ),
        migrations.AddField(
            model_name='category',
            name='posts',
            field=models.ManyToManyField(blank=True, related_name='categories', to='myblog.Post'),
        ),
        migrations.AddField(
            model_name='post',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myblog.Category'),
        ),
    ]
