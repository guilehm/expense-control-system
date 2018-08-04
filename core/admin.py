from django.contrib import admin

from core.models import Category, Tag


# Register your models here.
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    prepopulated_fields = {
        'slug': ('title',)
    }


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    prepopulated_fields = {
        'slug': ('title',)
    }


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
