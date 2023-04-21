from django.contrib import admin
from django.db.models import QuerySet, Count
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<15', 'Low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<15':
            return queryset.filter(inventory__lt=15)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'price', 'inventory_status', 'collection']
    list_editable = ['price']
    list_per_page = 10
    list_filter = ['collection', 'last_update', InventoryFilter]

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 15:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were succesfully updated!'
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
                reverse('admin:store_product_changelist')
                + '?'
                + urlencode({
            'collection__id': str(collection.id)
        })
        )

        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(selfself, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            products_count=Count('product')

        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    search_fields = ['first_name__startswith', 'last_name__startswith']
