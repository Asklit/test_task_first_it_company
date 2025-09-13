from rest_framework import viewsets
from ..models import Subcategory
from ..serializers import SubcategorySerializer

class SubcategoryViewSet(viewsets.ModelViewSet):
    
    """CRUD with modelviewset for subcategory"""

    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer