# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 15:03
from __future__ import unicode_literals

import book.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True)),
                ('date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('text', models.TextField()),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_name', models.CharField(db_index=True, max_length=32, unique=True)),
                ('name', models.CharField(max_length=32)),
                ('color', models.CharField(choices=[('deep-purple', 'Deep Purple'), ('indigo', 'Indigo'), ('lime', 'Lime'), ('teal', 'Teal'), ('red', 'Red'), ('green', 'Green'), ('orange', 'Orange'), ('yellow', 'Yellow'), ('blue', 'Blue'), ('light-blue', 'Light Blue'), ('cyan', 'Cyan'), ('light-green', 'Light Green'), ('amber', 'Amber'), ('deep-orange', 'Deep Orange'), ('purple', 'Purple'), ('pink', 'Pink')], default='cyan', max_length=16)),
                ('admins', models.ManyToManyField(related_name='admins_of', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='families', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Families',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('path', models.ImageField(upload_to=book.models.get_image_path)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('family', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='book.Family')),
            ],
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('key', models.CharField(db_index=True, max_length=32)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Family')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('address', models.CharField(max_length=80)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('birthday', models.DateField(blank=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='book.Location')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Family')),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='book.Image')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PollOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('votes', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_at', models.DateTimeField()),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('askers', models.ManyToManyField(related_name='wish_lists', to=settings.AUTH_USER_MODEL)),
                ('givers', models.ManyToManyField(related_name='giving_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WishListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=60)),
                ('link', models.URLField(blank=True)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.WishList')),
                ('purchaser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.Post')),
                ('date', models.DateTimeField()),
                ('ending_date', models.DateTimeField(null=True)),
            ],
            bases=('book.post',),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.Post')),
                ('url', models.URLField()),
            ],
            bases=('book.post',),
        ),
        migrations.CreateModel(
            name='MultiPhoto',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.Post')),
            ],
            bases=('book.post',),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.Post')),
            ],
            bases=('book.post',),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.Post')),
            ],
            bases=('book.post',),
        ),
        migrations.AddField(
            model_name='post',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='book.Family'),
        ),
        migrations.AddField(
            model_name='post',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Member'),
        ),
        migrations.AddField(
            model_name='post',
            name='read_by',
            field=models.ManyToManyField(related_name='read_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invite',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book.Member'),
        ),
        migrations.AddField(
            model_name='image',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='book.Location'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Post'),
        ),
        migrations.AddField(
            model_name='album',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Family'),
        ),
        migrations.AddField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(to='book.Image'),
        ),
        migrations.AddField(
            model_name='polloption',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Poll'),
        ),
        migrations.AddField(
            model_name='photo',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Image'),
        ),
        migrations.AddField(
            model_name='multiphoto',
            name='images',
            field=models.ManyToManyField(to='book.Image'),
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Image'),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Location'),
        ),
        migrations.AddField(
            model_name='album',
            name='event_at',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Event'),
        ),
    ]
