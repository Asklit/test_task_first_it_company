from rest_framework import serializers
from ..models import Subcategory, Category


class SubcategorySerializer(serializers.ModelSerializer):
    """Subcategory serializer"""

    root_category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'root_category']


class SubcategoryFilterSerializer(serializers.ModelSerializer):
    """Subcategory filter serializer"""
    
    class Meta:
        model = Subcategory
        fields = ['id', 'name']