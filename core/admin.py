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
    list_display = ('title', 'slug', 'owner')
    list_filter = ('owner', 'date_added',)
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(CSV)
class CSVAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'original_file_name', 'date_added', 'owner')
    list_filter = ('owner', 'date_added')
    search_fields = ('owner', 'file', 'original_file_name')
