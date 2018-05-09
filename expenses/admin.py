from django.contrib import admin
from expenses.models import Expense
from core.models import Tag

# Register your models here.
class TagInline(admin.StackedInline):
    model = Expense.tags.through
    extra = 0

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'category', 'paid_out',]
    list_filter = ['title', 'category', 'paid_out',]
    exclude = (
        ['tags',]
    )
    prepopulated_fields = {
        'slug': ('title',)
    }
    inlines = [
        TagInline,
    ]
