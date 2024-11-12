from django.contrib import admin
from .models import *

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1

class SeasonInline(admin.TabularInline):
    model = Season
    extra = 1
    show_change_link = True

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ['name', 'original_name', 'rating', 'year_of_manufacture', 'view_count', 'created_at', 'updated_at']
    list_filter = ['year_of_manufacture', 'rating', 'age_limit', 'status', 'studios']
    ordering = ['-year_of_manufacture', 'created_at', 'updated_at']
    list_editable = ['rating', 'view_count']
    inlines = [SeasonInline]
    filter_horizontal = ('genre', 'series_files')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Age)
class AgeAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ['studios_name', 'image']

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['anime', 'season_number', 'title']
    inlines = [EpisodeInline]

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['anime', 'season', 'episode_number', 'title']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'created_at', 'updated_at']
# Register your models here.
