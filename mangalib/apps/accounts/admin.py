from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'username',
        'avatar',
        'created_at',
    ]
    filter_horizontal = ('favorites', 'favorites_genre')
# Register your models here.
