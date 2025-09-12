from django.contrib import admin
from .models import Status, TransactionType, Category, Subcategory, Transaction
from django.contrib.admin import DateFieldListFilter
from transactions.validation import validate_transaction


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):

    """Status admin panel form"""

    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    
    """Transaction type admin panel form"""

    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    """Category admin panel form"""

    list_display = ('id', 'name', 'root_transaction_type')
    list_filter = ('root_transaction_type',)
    search_fields = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):

    """Subcategory admin panel form"""

    list_display = ('id', 'name', 'root_category')
    list_filter = ('root_category',)
    search_fields = ('name',)

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

    # fields for seach
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
        """Используем общую функцию валидации"""
        validate_transaction(obj)
        super().save_model(request, obj, form, change)