# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-16 18:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20161001_0748'),
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('reccuring', models.BooleanField()),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-posted_at']},
        ),
        migrations.RemoveField(
            model_name='member',
            name='birthday',
        ),
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='family',
            name='color',
            field=models.CharField(choices=[('green', 'Green'), ('amber', 'Amber'), ('light-blue', 'Light Blue'), ('deep-orange', 'Deep Orange'), ('deep-purple', 'Deep Purple'), ('blue', 'Blue'), ('teal', 'Teal'), ('lime', 'Lime'), ('red', 'Red'), ('light-green', 'Light Green'), ('orange', 'Orange'), ('yellow', 'Yellow'), ('purple', 'Purple'), ('pink', 'Pink'), ('cyan', 'Cyan'), ('indigo', 'Indigo')], default='cyan', max_length=16),
        ),
        migrations.AddField(
            model_name='date',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Family'),
        ),
        migrations.AddField(
            model_name='date',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Member'),
        ),
    ]
