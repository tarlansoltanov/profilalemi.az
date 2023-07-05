from django.contrib import admin

from .models import Color


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
