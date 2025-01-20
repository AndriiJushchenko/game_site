from django.contrib import admin
from .models import *

class GamesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'developer', 'date')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}

class PlatformsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Games, GamesAdmin)
admin.site.register(Platforms, PlatformsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Favorite)
