from django.contrib import admin
from ..models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    """Category admin panel form"""
    
    list_display = ('id', 'name', 'root_transaction_type')
    list_filter = ('root_transaction_type',)
    search_fields = ('name',)