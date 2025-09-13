from django.contrib import admin
from ..models import Status

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):

    """Status admin panel form"""
    
    list_display = ('id', 'name')
    search_fields = ('name',)