from django.contrib import admin

from core.models import Category, CSV, Tag


# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')
    list_filter = ('owner', 'date_added',)
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')
    list_filter = ('owner', 'date_added',)
    prepopulated_fields = {
        'slug': ('title',)
    }
