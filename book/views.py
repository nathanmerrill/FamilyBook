import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
import datetime
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import logout as logout_user, login as login_user, authenticate
from django.views.decorators.http import require_http_methods
import cloudinary.api
import cloudinary.uploader
import imghdr
import exifread

from book.models import *

DATE_TAG = "EXIF DateTimeOriginal"


def login(request: HttpRequest):
    user = request.user
    if request.method == 'POST':
        errors = process_login(request)
        if errors:
            request.session['errors'] = errors
            return redirect('login')
    if user.is_authenticated():
        if user.families.count() == 1:
            return redirect('family:home', family=user.families.first().url_name)
        return redirect('families')
    params = {
        'bg_image': random.sample(list(Upload.objects.filter(family=None)), 1)[0]
    }
    return render(request, 'book/global/login.html', params)


def process_login(request: HttpRequest):
    params = []
    username = request.POST['username']
    password = request.POST['password']
    if not username:
        params.append("Username required")
    if not password:
        params.append("Password required")
    if not username or not password:
        return params
    user = authenticate(username=username, password=password)
    if user is not None:
        login_user(request, user)
    else:
        params.append("Invalid username or password")
        return params


def home(request: HttpRequest, family: Family):
    paginator = Paginator(family.posts.all(), 50)
    try:
        posts = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'book/home.html', {"posts": posts, "family": family})


@login_required()
@require_http_methods("GET")
def standard_page(request: HttpRequest, **kwargs):
    return render(request, 'book/' + request.path.split("/")[-1] + ".html", kwargs)


def logout(request: HttpRequest):
    logout_user(request)
    return redirect("login")


@require_http_methods("GET")
def get_image(request: HttpRequest, path: str):
    image = get_object_or_404(Upload, path=path, is_image=True)
    if image.family:
        if not request.user.is_authenticated() or request.user not in image.family.users:
            raise Http404('Access Denied')
    image_data = open(image.path.path, "rb").read()
    return HttpResponse(image_data, content_type="image/jpg")


@login_required()
def batch_create(request: HttpRequest):
    if not request.user.is_superuser:
        return Http404('Access Denied')
    images = cloudinary.api.resources(type="upload", prefix="temples", max_results=500)
    save_all(Upload(family=None, path=image['public_id'], uploader=request.user, name=image['public_id'][0:32])
             for image in images['resources'])
    return HttpResponse('Success!')


def photo_view(request: HttpRequest, family: Family, photo: int):
    pass


def member_view(request: HttpRequest, family: Family, member: int):
    pass


@login_required()
def new_post(request: HttpRequest, family: Family):
    if request.method == "GET":
        return redirect('family:home', family=family.url_name)
    if not request.POST['content'] and not request.FILES:
        request.session['errors'] = ["Please add some content"]
        return redirect('family:home', family=family.url_name)

    post_type = Post
    kwargs = dict()
    if request.FILES:
        images = [create_upload(image) for image in request.FILES.getlist('file')]
        for image in images:
            image.family = family
            image.uploader = request.user
        if len(images) == 1:
            post_type = Photo
            image = images[0]
            kwargs['image'] = image
            image.save()

        elif len(images) > 1:
            post_type = MultiPhoto
            save_all(images)

    post = post_type(family=family,
                     user=request.user,
                     text=request.POST['content'],
                     **kwargs)
    post.save()
    if post_type == MultiPhoto:
        through_model = MultiPhoto.images.through
        # noinspection PyUnboundLocalVariable
        through_model.objects.bulk_create([
            through_model(upload_id=image.pk, multiphoto_id=post.pk)
            for image in images
        ])
    post.read_by.add(request.user)
    post.save()
    return redirect('family:home', family=family.url_name)


def create_upload(image):
    path = cloudinary.uploader.upload(image.file)['public_id']
    tags = exifread.process_file(image, stop_tag=DATE_TAG)
    if DATE_TAG in tags:
        date = datetime.datetime.strptime(tags[DATE_TAG].values, "%Y:%m:%d %H:%M:%S")
    else:
        date = datetime.datetime.now().date()
    upload = Upload(
        name=image.name,
        path=path,
        is_image=imghdr.what(image.file) in ('jpeg', 'gif', 'png'),
        date=date
    )
    return upload


@transaction.atomic
def save_all(items):
    for item in items:
        item.save()
