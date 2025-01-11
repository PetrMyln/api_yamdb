from django.contrib import admin


from reviews.models import (
    Comment,
    Review,
    MyUser,
    Categories,
    Title,
    Genre
)
# Register your models here.
admin.site.register(Title)
admin.site.register(Categories)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
