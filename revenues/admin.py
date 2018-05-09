from django.contrib import admin
from revenues.models import Revenue

# Register your models here.
class TagInline(admin.StackedInline):
    model = Revenue.tags.through
    extra = 0

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'category', 'received_out',]
    list_filter = ['title', 'category', 'received_out',]
    exclude = (
        ['tags',]
    )
    prepopulated_fields = {
        'slug': ('title',)
    }
    inlines = [
        TagInline,
    ]
