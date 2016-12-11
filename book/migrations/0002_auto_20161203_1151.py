# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-03 18:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='family',
            name='cloudinary_name',
        ),
        migrations.RemoveField(
            model_name='family',
            name='color',
        ),
        migrations.AlterField(
            model_name='post',
            name='posted_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]