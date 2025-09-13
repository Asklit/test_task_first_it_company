from django.contrib import admin
from ..models import TransactionType

@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):

    """Transaction type admin panel form"""
    
    list_display = ('id', 'name')
    search_fields = ('name',)