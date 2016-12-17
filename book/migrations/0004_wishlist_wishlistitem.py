# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-17 13:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_auto_20161217_0608'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('askers', models.ManyToManyField(related_name='wish_lists', to='book.Member')),
                ('givers', models.ManyToManyField(related_name='giving_to', to='book.Member')),
            ],
        ),
        migrations.CreateModel(
            name='WishListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=60)),
                ('link', models.URLField(blank=True)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.WishList')),
                ('purchaser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='book.Member')),
            ],
        ),
    ]
