import random

from django.db import transaction
from django.utils import timezone
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import logout as logout_user, login as login_user, authenticate
from django.views.decorators.http import require_http_methods

from book.models import *


def login(request: HttpRequest):
    user = request.user
    if request.method == 'POST':
        errors = process_login(request)
        if errors:
            return errors
    if user.is_authenticated():
        if user.families.count() == 1:
            return redirect('family:home', family=user.families.first().url_name)
        return redirect('families')
    params = {'bg_image': random.sample(list(Image.objects.filter(family=None)), 1)[0]}
    return render(request, 'book/global/login.html', params)


def process_login(request: HttpRequest):
    params = {}
    username = request.POST['username']
    password = request.POST['password']
    if not username:
        params['username'] = "Username required"
    if not password:
        params['password'] = "Password required"
    if not username or not password:
        return JsonResponse(params, status=422)
    user = authenticate(username=username, password=password)
    if user is not None:
        login_user(request, user)
    else:
        params['errors'] = "Invalid username or password"
        return JsonResponse(params, status=422)


@login_required()
@require_http_methods("GET")
def standard_page(request: HttpRequest, **kwargs):
    return render(request, 'book/' + request.path.split("/")[-1] + ".html", kwargs)


def logout(request: HttpRequest):
    logout_user(request)
    return redirect("login")


@require_http_methods("GET")
def get_image(request: HttpRequest, path: str):
    image = get_object_or_404(Image, path=path)
    if image.family:
        if not request.user.is_authenticated() or request.user not in image.family.users:
            raise Http404('Access Denied')
    image_data = open(image.path.path, "rb").read()
    return HttpResponse(image_data, content_type="image/jpg")


@login_required()
def batch_create(request: HttpRequest):
    if not request.user.is_superuser:
        return Http404('Access Denied')
    images = [
        "aba-nigeria-temple-lds-273999-wallpaper.jpg",
        "manila-philippines-temple-lds-919379-wallpaper.jpg",
        "abuquerque-temple-lds-820684-wallpaper.jpg",
        "manti-utah-temple-night-1075642-wallpaper.jpg",
        "accra-ghana-temple-lds-249026-wallpaper.jpg",
        "medford-temple-lds-988399-wallpaper.jpg",
        "adelaide-australia-temple-lds-776369-wallpaper.jpg",
        "melbourne-australia-temple-lds-1636402-wallpaper.jpg",
        "anchorage-temple-lds-746769-wallpaper.jpg",
        "memphis-tennessee-temple-1349053-wallpaper.jpg",
        "apia-samoa-temple-lds-495972-wallpaper.jpg",
        "merida-mexico-temple-lds-643985-wallpaper.jpg",
        "asuncion-paraguay-temple-lds-249034-wallpaper.jpg",
        "mesa-temple-reflection-683429-wallpaper.jpg",
        "atlanta-georgia-mormon-temple-900182-wallpaper.jpg",
        "mexico-city-temple-exterior-1518357-wallpaper.jpg",
        "baton-rouge-temple-lds-1029727-wallpaper.jpg",
        "monterrey-mexico-temple-lds-126690-wallpaper.jpg",
        "bern-switzerland-temple-lds-653038-wallpaper.jpg",
        "montevideo-uruguay-temple-lds-83476-wallpaper.jpg",
        "billings-temple-lds-946466-wallpaper.jpg",
        "monticello-temple-lds-1157281-wallpaper.jpg",
        "birmingham-alabama-temple-lds-83482-wallpaper.jpg",
        "montreal-quebec-temple-lighted-1169263-wallpaper.jpg",
        "bismarck-temple-lds-829428-wallpaper.jpg",
        "mount-timpanogos-temple-lds-885511-wallpaper.jpg",
        "bogota-colombia-mormon-temple-856490-wallpaper.jpg",
        "nashville-tennessee-mormon-temple-1121445-wallpaper.jpg",
        "boise-idaho-temple-lds-1012653-wallpaper.jpg",
        "nauvoo-temple-756496-wallpaper.jpg",
        "boston-temple-lds-945541-wallpaper.jpg",
        "newport-beach-temple-lds-917306-wallpaper.jpg",
        "bountiful-temple-lds-1059079-wallpaper.jpg",
        "nukualofa-tonga-temple-lds-445030-wallpaper.jpg",
        "brigham-city-utah-temple-dawn-1093979-wallpaper.jpg",
        "oakland-california-temple-golden-sunset-1021130-wallpaper.jpg",
        "brisbane-australia-temple-lds-745088-wallpaper.jpg",
        "oaxaca-mexico-temple-759274-wallpaper.jpg",
        "buenos-aires-argentina-temple-lds-82744-wallpaper.jpg",
        "ogden-temple-exterior-lds-1265931-wallpaper.jpg",
        "calgary-alberta-temple-lds-1025065-wallpaper.jpg",
        "oklahoma-temple-lds-130142-wallpaper.jpg",
        "campinas-brazil-temple-lighted-1029894-wallpaper.jpg",
        "oquirrh-mountain-temple-lds-885895-wallpaper.jpg",
        "caracas-mormon-temple8.jpg",
        "orlando-temple-lds-828935-wallpaper.jpg",
        "cardston-alberta-temple-exterior-1126230-wallpaper.jpg",
        "palmyra-new-york-mormon-temple-882900-wallpaper.jpg",
        "chicago-temple-lds-885844-wallpaper.jpg",
        "panama-city-temple-lds-569185-wallpaper.jpg",
        "ciudad-juarez-mexico-temple-lds-126122-wallpaper.jpg",
        "papeete-tahiti-temple-1232272-wallpaper.jpg",
        "cochabamba-mormon-temple9.jpg",
        "payson-temple-daylight-1416668-wallpaper.jpg",
        "colonia-juarez-chihuahua-mexico-temple-1543027-wallpaper.jpg",
        "perth-australia-temple-1562613-wallpaper.jpg",
        "columbia-river-temple-lds-761262-wallpaper.jpg",
        "philadelphia-pennsylvania-temple-exterior-1775822-wallpaper.jpg",
        "columbia-temple-768161-wallpaper.jpg",
        "philippines-cebu-temple-1334564-wallpaper.jpg",
        "columbus-temple-lds-406110-wallpaper.jpg",
        "phoenix-arizona-temple-exterior-1300742-wallpaper.jpg",
        "copenhagen-denmark-temple-lds-278232-wallpaper.jpg",
        "portland-temple-lds-1079112-wallpaper.jpg",
        "cordoba-argentina-temple-rendering-780527-wallpaper.jpg",
        "porto-alegre-brazil-temple-lds-83426-wallpaper.jpg",
        "curitiba-brazil-temple-lds-852263-wallpaper.jpg",
        "preston-temple-765117-wallpaper.jpg",
        "dallas-temple-lds-850748-wallpaper.jpg",
        "provo-city-center-temple-1572517-wallpaper.jpg",
        "denver-colorado-temple-lds-845690-wallpaper.jpg",
        "provo-temple-lds-890642-wallpaper.jpg",
        "detroit-temple-766397-wallpaper.jpg",
        "quetzaltenango-guatemala-temple-art-lds-640706-wallpaper.jpg",
        "draper-utah-lds-temple-942143-wallpaper.jpg",
        "raliegh-temple-lds-894677-wallpaper.jpg",
        "edmonton-alberta-temple-lds-854741-wallpaper.jpg",
        "recife-brazil-temple-lds-700205-wallpaper.jpg",
        "exterior-sapporo-japan-temples-1744806-wallpaper.jpg",
        "redlands-temple-lds-165642-wallpaper.jpg",
        "fortaleza-brazil-temple-lds-950796-wallpaper.jpg",
        "regina-saskatchewan-temple-lds-1027275-wallpaper.jpg",
        "fort-collins-colorado-temple-morning-exterior-1776055-wallpaper.jpg",
        "reno-temple-lds-129847-wallpaper.jpg",
        "fort-lauderdale-florida-temple-1220610-wallpaper.jpg",
        "rexburg-idaho-temple-storm-clouds-1096114-wallpaper.jpg",
        "frankfurt-germany-temple-lds-82734-wallpaper.jpg",
        "rome-italy-temple-rendering-780525-wallpaper.jpg",
        "freiberg-germany-temple-lds-664670-wallpaper.jpg",
        "sacramento-temple-769989-wallpaper.jpg",
        "fresno-temple-lds-935867-wallpaper.jpg",
        "salt-lake-temple-christmas-1136121-wallpaper.jpg",
        "fukuoka-japan-temple-lds-306863-wallpaper.jpg",
        "san-antonio-temple-lds-884475-wallpaper.jpg",
        "gila-valley-temple-lds-810267-wallpaper.jpg",
        "san-diego-california-temple-grounds-1164680-wallpaper.jpg",
        "gilbert-arizona-temple-1554530-wallpaper.jpg",
        "san-jose-costa-rica-temple-lds-1006824-wallpaper.jpg",
        "guadalajara-temple-lds-1643018-wallpaper.jpg",
        "san-salvador-el-salvadot-temple-lds-848548-wallpaper.jpg",
        "guayaquil-ecuador-temple-lds-884499-wallpaper.jpg",
        "santiago-chile-lds-temple-1085562-wallpaper.jpg",
        "hague-netherlands-mormon-temple-1088316-wallpaper.jpg",
        "santo-domingo-dominican-republic-temple-lds-935262-wallpaper.jpg",
        "halifax-nova-scotia-lds-temple-942187-wallpaper.jpg",
        "sao-paulo-brazil-temple-lds-246609-wallpaper.jpg",
        "hamilton-new-zealand-lds-temple-942155-wallpaper.jpg",
        "seatlle-temple-lds-933557-wallpaper.jpg",
        "helsinki-finland-temple-lds-354498-wallpaper.jpg",
        "seoul-korea-temple-lds-424784-wallpaper.jpg",
        "hermosillo-mexico-temple-lds-171162-wallpaper.jpg",
        "snowflake-temple-lds-845142-wallpaper.jpg",
        "hong-kong-china-temple-lds-992548-wallpaper.jpg",
        "spokane-temple-lds-736590-wallpaper.jpg",
        "houston-texas-mormon-temple-907828-wallpaper.jpg",
        "st-george-utah-temple-clouds-922212-wallpaper.jpg",
        "idaho-falls-temple-lds-845209-wallpaper.jpg",
        "st-louis-temple-lds-850421-wallpaper.jpg",
        "indianapolis-indiana-temple-1484557-wallpaper.jpg",
        "stockholm-sweden-lds-temple-1029788-wallpaper.jpg",
        "johannesburg-south-africa-temple-lds-375190-wallpaper.jpg",
        "st-paul-minnesota-lds-temple-1160303-wallpaper.jpg",
        "jordan-river-temple-lds-924754-wallpaper.jpg",
        "suva-fiji-temple-lds-264818-wallpaper.jpg",
        "kansas-city-temple-lds-911027-wallpaper.jpg",
        "sydney-australia-temple-sunset-1116152-wallpaper.jpg",
        "kirtland-temple-677286-wallpaper.jpg",
        "taipei-taiwan-temple-lds-1672186-wallpaper.jpg",
        "kona-temple-lds-83401-wallpaper.jpg",
        "tampico-mexico-temple-lds-129825-wallpaper.jpg",
        "kyiv-ukraine-temple-lds-774302-wallpaper.jpg",
        "tegucigalpa-honduras-temple-lds-1075376-wallpaper.jpg",
        "laie-temple-772757-wallpaper.jpg",
        "tijuana-mexico-temple-rendering-1506624-wallpaper.jpg",
        "las-vegas-temple-lds-758798-wallpaper.jpg",
        "tokyo-japan-temple-lds-736267-wallpaper.jpg",
        "lds-temple-guatemala-city-1021144-wallpaper.jpg",
        "toronto-temple-lds-817787-wallpaper.jpg",
        "lima-peru-temple-lds-894713-wallpaper.jpg",
        "trujillo-peru-temple-exterior-1449769-wallpaper.jpg",
        "logan-temple-768119-wallpaper.jpg",
        "tuxtla-gutierrez-mormon-temple2.jpg",
        "london-england-temple-lds-393730-wallpaper.jpg",
        "twin-falls-temple-769943-wallpaper.jpg",
        "los-angeles-california-temple-1079458-wallpaper.jpg",
        "vancouver-temple-lds-866777-wallpaper.jpg",
        "louisville-temple-lds-1027646-wallpaper.jpg",
        "veracruz-mexico-temple-lds-83516-wallpaper.jpg",
        "lubbock-temple-lds-126691-wallpaper.jpg",
        "vernal-temple-lds-39491-wallpaper.jpg",
        "madrid-spain-mormon-temple-954942-wallpaper.jpg",
        "villahermosa-mexico-temple-lds-83484-wallpaper.jpg",
        "manaus-brazil-temple-lds-1481221-wallpaper.jpg",
        "washington-dc-temple-lds-770751-wallpaper.jpg",
        "manhattan-temple-lds-248728-wallpaper.jpg",
        "winter-quarters-temple-lds-772766-wallpaper.jpg"
    ]
    names = [
        "Aba Nigeria Temple",
        "Manila Philippines Temple",
        "Abuquerque Temple",
        "Manti Utah Temple",
        "Accra Ghana Temple",
        "Medford Temple",
        "Adelaide Australia Temple",
        "Melbourne Australia Temple",
        "Anchorage Temple",
        "Memphis Tennessee Temple",
        "Apia Samoa Temple",
        "Merida Mexico Temple",
        "Asuncion Paraguay Temple",
        "Mesa Temple",
        "Atlanta Georgia Temple",
        "Mexico City Temple",
        "Baton Rouge Temple",
        "Monterrey Mexico Temple",
        "Bern Switzerland Temple",
        "Montevideo Uruguay Temple",
        "Billings Temple",
        "Monticello Temple",
        "Birmingham Alabama Temple",
        "Montreal Quebec Temple",
        "Bismarck Temple",
        "Mount Timpanogos Temple",
        "Bogota Colombia Temple",
        "Nashville Tennessee Temple",
        "Boise Idaho Temple",
        "Nauvoo Temple",
        "Boston Temple",
        "Newport Beach Temple",
        "Bountiful Temple",
        "Nukualofa Tonga Temple",
        "Brigham City Utah Temple",
        "Oakland California Temple",
        "Brisbane Australia Temple",
        "Oaxaca Mexico Temple",
        "Buenos Aires Argentina Temple",
        "Ogden Temple",
        "Calgary Alberta Temple",
        "Oklahoma Temple",
        "Campinas Brazil Temple",
        "Oquirrh Mountain Temple",
        "Caracas Temple",
        "Orlando Temple",
        "Cardston Alberta Temple",
        "Palmyra New York Temple",
        "Chicago Temple",
        "Panama City Temple",
        "Ciudad Juarez Mexico Temple",
        "Papeete Tahiti Temple",
        "Cochabamba Temple",
        "Payson Temple",
        "Colonia Juarez Chihuahua Mexico Temple",
        "Perth Australia Temple",
        "Columbia River Temple",
        "Philadelphia Pennsylvania Temple",
        "Columbia Temple",
        "Philippines Cebu Temple",
        "Columbus Temple",
        "Phoenix Arizona Temple",
        "Copenhagen Denmark Temple",
        "Portland Temple",
        "Cordoba Argentina Temple",
        "Porto Alegre Brazil Temple",
        "Curitiba Brazil Temple",
        "Preston Temple",
        "Dallas Temple",
        "Provo City Center Temple",
        "Denver Colorado Temple",
        "Provo Temple",
        "Detroit Temple",
        "Quetzaltenango Guatemala Temple",
        "Draper Utah Temple",
        "Raliegh Temple",
        "Edmonton Alberta Temple",
        "Recife Brazil Temple",
        "Exterior Sapporo Japan Temple",
        "Redlands Temple",
        "Fortaleza Brazil Temple",
        "Regina Saskatchewan Temple",
        "Fort Collins Colorado Temple",
        "Reno Temple",
        "Fort Lauderdale Florida Temple",
        "Rexburg Idaho Temple",
        "Frankfurt Germany Temple",
        "Rome Italy Temple",
        "Freiberg Germany Temple",
        "Sacramento Temple",
        "Fresno Temple",
        "Salt Lake Temple",
        "Fukuoka Japan Temple",
        "San Antonio Temple",
        "Gila Valley Temple",
        "San Diego California Temple",
        "Gilbert Arizona Temple",
        "San Jose Costa Rica Temple",
        "Guadalajara Temple",
        "San Salvador El Salvadot Temple",
        "Guayaquil Ecuador Temple",
        "Santiago Chile Temple",
        "Hague Netherlands Temple",
        "Santo Domingo Dominican Republic Temple",
        "Halifax Nova Scotia Temple",
        "Sao Paulo Brazil Temple",
        "Hamilton New Zealand Temple",
        "Seatlle Temple",
        "Helsinki Finland Temple",
        "Seoul Korea Temple",
        "Hermosillo Mexico Temple",
        "Snowflake Temple",
        "Hong Kong China Temple",
        "Spokane Temple",
        "Houston Texas Temple",
        "St George Utah Temple",
        "Idaho Falls Temple",
        "St Louis Temple",
        "Indianapolis Indiana Temple",
        "Stockholm Sweden Temple",
        "Johannesburg South Africa Temple",
        "St Paul Minnesota Temple",
        "Jordan River Temple",
        "Suva Fiji Temple",
        "Kansas City Temple",
        "Sydney Australia Temple",
        "Kirtland Temple",
        "Taipei Taiwan Temple",
        "Kona Temple",
        "Tampico Mexico Temple",
        "Kyiv Ukraine Temple",
        "Tegucigalpa Honduras Temple",
        "Laie Temple",
        "Tijuana Mexico Temple",
        "Las Vegas Temple",
        "Tokyo Japan Temple",
        "Guatemala City Temple",
        "Toronto Temple",
        "Lima Peru Temple",
        "Trujillo Peru Temple",
        "Logan Temple",
        "Tuxtla Gutierrez Temple",
        "London England Temple",
        "Twin Falls Temple",
        "Los Angeles California Temple",
        "Vancouver Temple",
        "Louisville Temple",
        "Veracruz Mexico Temple",
        "Lubbock Temple",
        "Vernal Temple",
        "Madrid Spain Temple",
        "Villahermosa Mexico Temple",
        "Manaus Brazil Temple",
        "Washington DC Temple",
        "Manhattan Temple",
        "Winter Quarters Temple"
    ]
    temples = zip(images, names)
    for image, name in temples:
        Image(family=None, name=name, path=image).save()
    return HttpResponse('Success!')


def photo_view(request: HttpRequest, family: Family, photo: int):
    pass


def member_view(request: HttpRequest, family: Family, member: int):
    pass


@login_required()
@require_http_methods("POST")
def new_post(request: HttpRequest, family: Family):
    if 'content' not in request.POST or not request.POST['content']:
        return HttpResponseBadRequest("Content required")

    post_type = Post
    kwargs = dict()
    if request.FILES:
        images = [
            Image(family=family, name=name, path=image, date=timezone.now)
            for name, image
            in request.FILES
            ]
        if len(images) == 1:
            post_type = Photo
            kwargs['image'] = images[0]
        elif len(images) > 1:
            post_type = MultiPhoto
            save_all(images)
            kwargs['images'] = images

    post = post_type(family=family,
                     user=request.user,
                     posted_at=timezone.now(),
                     text=request.POST['content'],
                     **kwargs)
    post.save()
    post.read_by.add(request.user)
    post.save()
    return redirect('family:home', family=family.url_name)


@transaction.atomic
def save_all(items):
    for item in items:
        item.save()
