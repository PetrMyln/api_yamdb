from django.contrib import admin


from reviews.models import (
    Comment,
    Review,
    MyUser,
    Categories,
    Titles,
    Genre
)
# Register your models here.
admin.site.register(Titles)
admin.site.register(Categories)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
