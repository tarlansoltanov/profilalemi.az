from django.contrib import admin

from .models import Product, ProductName


@admin.register(ProductName)
class ProductNameAdmin(admin.ModelAdmin):
    """Admin definition for ProductName."""

    list_display = ('name', 'created_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin definition for Product."""

    list_display = ('name', 'color', 'created_at')
    list_filter = ('name', 'color', 'created_at')
    search_fields = ('name', 'color')
    sortable_by = ('name', 'color', 'created_at')
    ordering = ('created_at',)