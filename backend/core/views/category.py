from rest_framework import viewsets
from ..models import Category
from ..serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    
    """CRUD with modelviewset for category"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer