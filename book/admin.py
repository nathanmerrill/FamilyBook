from django.contrib import admin
from book import models as book_models

admin.site.register(book_models.Family)
admin.site.register(book_models.Member)
admin.site.register(book_models.Post)
admin.site.register(book_models.Invite)
admin.site.register(book_models.Image)
admin.site.register(book_models.Album)