import os

import datetime
from django.db import models
from django.contrib.auth.models import User
from book import services

colors = {
    "red":          "Red",
    "pink":         "Pink",
    "purple":       "Purple",
    "deep-purple":  "Deep Purple",
    "indigo":       "Indigo",
    "blue":         "Blue",
    "light-blue":   "Light Blue",
    "cyan":         "Cyan",
    "teal":         "Teal",
    "green":        "Green",
    "light-green":  "Light Green",
    "lime":         "Lime",
    "yellow":       "Yellow",
    "amber":        "Amber",
    "orange":       "Orange",
    "deep-orange":  "Deep Orange"
}


class Family(models.Model):
    url_name = models.CharField(max_length=32, unique=True, db_index=True)
    name = models.CharField(max_length=32)
    users = models.ManyToManyField(User, related_name="families")
    admins = models.ManyToManyField(User, related_name="admins_of")
    color = models.CharField(max_length=16, default='cyan', choices=colors.items())

    class Meta:
        verbose_name_plural = "Families"

    def __str__(self):
        return self.name

    def recent_messages(self, user: User):
        return services.recent_messages(user, self)

    def member(self, user: User):
        return Member.objects.get(family=self, user=user)

    def upcoming_events_and_dates(self):
        events = Event.objects.filter(family=self, date__gte=datetime.datetime.now().date())
        dates = Date.objects.filter(family=self, date__gte=datetime.datetime.now().date())
        combined = list(events) + list(dates)
        combined.sort(key=lambda a: a.date)
        return combined


class Member(models.Model):
    family = models.ForeignKey(Family)
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, null=True)
    address = models.ForeignKey('Location', blank=True, null=True)
    photo = models.ForeignKey('Image', blank=True, null=True)

    def __str__(self):
        return self.name


class Invite(models.Model):
    family = models.ForeignKey(Family)
    member = models.ForeignKey(Member, null=True)
    email = models.EmailField()
    key = models.CharField(max_length=32, db_index=True)

    def __str__(self):
        return "Invite to "+self.email


class Post(models.Model):
    family = models.ForeignKey(Family, related_name="posts")
    user = models.ForeignKey(User)
    posted_at = models.DateTimeField()
    text = models.TextField()
    read_by = models.ManyToManyField(User, related_name="read_posts")

    class Meta:
        ordering = ['-posted_at']

    def member(self):
        return self.user.member_set.get(family=self.family)


class Link(Post):
    url = models.URLField()


class Poll(Post):
    pass


class PollOption(models.Model):
    poll = models.ForeignKey(Poll)
    name = models.CharField(max_length=32)
    votes = models.ManyToManyField(User)


class Photo(Post):
    image = models.ForeignKey('Image')


class MultiPhoto(Post):
    images = models.ManyToManyField('Image')


class Event(Post):
    date = models.DateTimeField()
    image = models.ForeignKey('Image')
    name = models.CharField(max_length=32)
    ending_date = models.DateTimeField(null=True)
    location = models.ForeignKey('Location')


class Comment(models.Model):
    post = models.ForeignKey(Post)
    commenter = models.ForeignKey(User)
    time = models.DateTimeField()
    text = models.TextField()


class Album(models.Model):
    family = models.ForeignKey(Family)
    photos = models.ManyToManyField('Image')
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    date = models.DateField(null=True)
    event_at = models.ForeignKey('Event')


class WishList(models.Model):
    askers = models.ManyToManyField(User, related_name="wish_lists")
    name = models.CharField(max_length=60)
    givers = models.ManyToManyField(User, related_name="giving_to")


class WishListItem(models.Model):
    list = models.ForeignKey(WishList)
    item = models.CharField(max_length=60)
    link = models.URLField(blank=True)
    purchaser = models.ForeignKey(User, null=True, blank=True)


class Location(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=80)
    latitude = models.FloatField()
    longitude = models.FloatField()
    # https://developers.google.com/maps/articles/phpsqlsearch_v3


def get_image_path(instance: 'Image', filename: str):
    ext_index = filename.rfind('.')
    return os.path.join('uploads/images', filename[:ext_index]+'-'+str(instance.id)+filename[ext_index+1:])


class Image(models.Model):
    family = models.ForeignKey(Family, null=True, blank=True)
    name = models.CharField(max_length=32)
    path = models.ImageField(upload_to=get_image_path)
    date = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)

    def __str__(self):
        return self.name


class Date(models.Model):
    family = models.ForeignKey(Family)
    user = models.ForeignKey(Member)
    date = models.DateField()
    reccuring = models.BooleanField()
    name = models.CharField(max_length=32)
