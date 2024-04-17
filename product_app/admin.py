from django.utils.html import format_html

from django.contrib import admin
from .models import *


# Seach with suggession demo db
# admin.site.register(Names)


# Brand admin page
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "display_image",
        "is_active",
        "offer_is_active",
        "offer_percentage",
    )
    list_filter = ("is_active", "offer_is_active")
    search_fields = ("name", "description")

    def display_image(self, obj):
        if obj.image:
            width = 50
            height = int(obj.image.height * (width / obj.image.width))
            return format_html(
                '<img src="{}" width="{}" height="{}" />'.format(
                    obj.image.url, width, height
                )
            )
        else:
            return ""

    display_image.short_description = "Image"


admin.site.register(Brand, BrandAdmin)


# Category admin page
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "display_image", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")

    def display_image(self, obj):
        if obj.image:
            width = 50
            height = int(obj.image.height * (width / obj.image.width))
            return format_html(
                '<img src="{}" width="{}" height="{}" />'.format(
                    obj.image.url, width, height
                )
            )
        else:
            return ""

    display_image.short_description = "Image"


admin.site.register(Category, CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "short_description",
        "display_image",
        "is_active",
    )
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")

    def short_description(self, obj):
        max_length = 50  # Maximum characters to display
        if len(obj.description) > max_length:
            return obj.description[:max_length] + "..."
        else:
            return obj.description

    short_description.short_description = "Description"

    def display_image(self, obj):
        if obj.image:
            # Calculate the height while maintaining the aspect ratio
            width = 50
            height = int(obj.image.height * (width / obj.image.width))
            return format_html(
                '<img src="{}" width="{}" height="{}" />'.format(
                    obj.image.url, width, height
                )
            )
        else:
            return ""

    display_image.short_description = "Image"


admin.site.register(Subcategory, SubcategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "short_description",
        "category",
        "sub_category",
        "mrp",
        "display_image",
        "availability",
        "stock",
        "sell_count",
        "date_added",
        "varient",
        "offer_is_active",
        "offer_percentage",
    )
    list_filter = (
        "brand",
        "category",
        "sub_category",
        "availability",
        "varient",
        "offer_is_active",
    )
    search_fields = ("name", "description")

    def short_description(self, obj):
        max_length = 30
        if len(obj.description) > max_length:
            return obj.description[:max_length] + "..."
        else:
            return obj.description

    short_description.short_description = "Description"

    def display_image(self, obj):
        if obj.image:
            # Calculate the height while maintaining the aspect ratio
            width = 50
            height = int(obj.image.height * (width / obj.image.width))
            return format_html(
                '<img src="{}" width="{}" height="{}" />'.format(
                    obj.image.url, width, height
                )
            )
        else:
            return ""

    display_image.short_description = "Image"


admin.site.register(Product, ProductAdmin)
