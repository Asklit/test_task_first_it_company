from django.contrib import admin
from ..models import Subcategory

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    
    """Subcategory admin panel form"""

    list_display = ('id', 'name', 'root_category')
    list_filter = ('root_category',)
    search_fields = ('name',)