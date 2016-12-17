import datetime

from django.db import models
from django.contrib.auth.models import User
from book import services
import cloudinary.models as cloudinary_models
from django.utils.crypto import get_random_string


class Family(models.Model):
    url_name = models.CharField(max_length=32, unique=True, db_index=True)
    name = models.CharField(max_length=32)
    users = models.ManyToManyField(User, related_name="families")
    admins = models.ManyToManyField(User, related_name="admins_of")

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
    photo = models.ForeignKey('Upload', blank=True, null=True)

    def __str__(self):
        return self.name


class Invite(models.Model):
    family = models.ForeignKey(Family)
    member = models.ForeignKey(Member, null=True)
    email = models.EmailField()
    key = models.CharField(max_length=32, db_index=True, default=lambda: get_random_string(32))

    def __str__(self):
        return "Invite to "+self.email


class Post(models.Model):
    family = models.ForeignKey(Family, related_name="posts")
    user = models.ForeignKey(User)
    posted_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    read_by = models.ManyToManyField(User, related_name="read_posts")
    featured = models.BooleanField(default=False)

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
    image = models.ForeignKey('Upload')


class File(Post):
    upload = models.ForeignKey('Upload')


class MultiPhoto(Post):
    images = models.ManyToManyField('Upload')


class Event(Post):
    date = models.DateTimeField()
    image = models.ForeignKey('Upload')
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
    photos = models.ManyToManyField('Upload')
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    date = models.DateField(null=True)
    event_at = models.ForeignKey('Event', null=True)


class WishList(models.Model):
    askers = models.ManyToManyField(Member, related_name="wish_lists")
    name = models.CharField(max_length=60)
    givers = models.ManyToManyField(Member, related_name="giving_to")


class WishListItem(models.Model):
    list = models.ForeignKey(WishList)
    item = models.CharField(max_length=60)
    link = models.URLField(blank=True)
    purchaser = models.ForeignKey(Member, null=True, blank=True)


class Location(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=80)
    latitude = models.FloatField()
    longitude = models.FloatField()
    # https://developers.google.com/maps/articles/phpsqlsearch_v3


class Upload(models.Model):
    family = models.ForeignKey(Family, null=True)
    name = models.CharField(max_length=32)
    uploader = models.ForeignKey(User)
    is_image = models.BooleanField(default=True)
    date = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    path = cloudinary_models.CloudinaryField()

    def small_url(self):
        path = str(self.path.url)
        parts = path.split("upload/")
        return parts[0] + "upload/c_fill,h_150,w_135/" + parts[1]

    def profile_url(self):
        path = str(self.path.url)
        parts = path.split("upload/")
        return parts[0] + "upload/w_50/" + parts[1]

    def __str__(self):
        return self.name


class Date(models.Model):
    family = models.ForeignKey(Family)
    user = models.ForeignKey(Member)
    date = models.DateField()
    reccuring = models.BooleanField()
    name = models.CharField(max_length=32)
