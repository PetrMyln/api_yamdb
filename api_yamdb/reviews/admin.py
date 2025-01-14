from django.contrib import admin

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)


class ReviewInLine(admin.StackedInline):
    model = Review
    extra = 0

class GenreInLine(admin.TabularInline):
    model = Title
    extra = 0


class TitleAdmin(admin.ModelAdmin):
    inlines = (ReviewInLine,)
    list_display = (
        'name',
        'year',
        # 'rating',
        'description',
        # 'genres_list',
        'category',
    )
    list_select_related = ('category', )
    list_editable = (
        # 'genre',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('category',)
    list_display_links = ('name',)
    filter_horizontal = ('genre',)
    

    # @admin.display(description='Genre list')
    # def genres_list(self, obj):
    #     return Genre.objects.all().filter('title_id')
    #     return obj.genre

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'title', 'score', 'pub_date')

    search_fields = ('text', 'author', 'title',)
    # list_filter = ('category',)
    list_display_links = ('text', )
   
    

admin.site.empty_value_display = '(None)'
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
