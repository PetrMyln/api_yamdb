from django.contrib import admin
from reviews.models import Category, Comment, Genre, Review, Title


class ReviewInLine(admin.StackedInline):
    model = Review
    extra = 0


class TitleAdmin(admin.ModelAdmin):
    inlines = (ReviewInLine,)
    list_display = (
        'name',
        'year',
        'description',
        'get_genres_list',
        'category',
    )
    list_select_related = ('category',)
    list_editable = (
        'category',
    )
    search_fields = ('name',)
    list_filter = ('category',)
    list_display_links = ('name',)
    filter_horizontal = ('genre',)

    @admin.display(description='Список жанров')
    def get_genres_list(self, obj):
        sqn_of_genre = Genre.objects.all().prefetch_related(
            'titles').filter(titles__id=obj.pk)
        genre_sqn = [curent for curent in sqn_of_genre]
        return genre_sqn if genre_sqn else 'Добавте жанры к произведению'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'title', 'score')
    search_fields = ('text', 'author__username', 'title__name',)
    list_display_links = ('text',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author')
    search_fields = ('text', 'author__username')

class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


admin.site.empty_value_display = '(None)'
admin.site.register(Category, CategoryGenreAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, CategoryGenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
