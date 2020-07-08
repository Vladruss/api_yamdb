from django.contrib import admin

from api.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
    empty_value_display = "-пусто-"
