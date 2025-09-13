from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from ..models import Transaction
from core.services.transaction_validation import validate_transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    """Transaction admin panel form"""
    
    list_display = (
        'id',
        'amount',
        'create_date',
        'status',
        'transaction_type',
        'category',
        'subcategory'
    )

    # Filters to display in admin panel
    list_filter = (
        'status',
        'transaction_type',
        'category',
        'subcategory',
        ('create_date', DateFieldListFilter),
    )

    # fields for search
    search_fields = (
        'notes',
        'amount',
        'create_date',
        'status__name', 
        'transaction_type__name',
        'category__name',
        'subcategory__name', 
    )
    date_hierarchy = 'create_date'

    def save_model(self, request, obj, form, change):
        
        """Use validate function"""

        validate_transaction(obj)
        super().save_model(request, obj, form, change)