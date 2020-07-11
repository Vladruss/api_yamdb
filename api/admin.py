from django.contrib import admin

from api.models import User, Title, Category, Genre, Review, Comment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
    empty_value_display = "-пусто-"


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'year','description')
    empty_value_display = "-пусто-"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    empty_value_display = "-пусто-"

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    empty_value_display = "-пусто-"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'score', 'pub_date', 'title_id')
    empty_value_display = "-пусто-"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ( 'text', 'author', 'pub_date')
    empty_value_display = "-пусто-"
