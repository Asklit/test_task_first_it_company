from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Subcategory
from ..serializers import SubcategoryFilterSerializer

class SubcategoryFilterView(APIView):
    
    """Filter for category"""
    
    def get(self, request):
        category_id = request.query_params.get('category_id')
        if category_id:
            subcategories = Subcategory.objects.filter(root_category_id=category_id)
        else:
            subcategories = Subcategory.objects.all()
        serializer = SubcategoryFilterSerializer(subcategories, many=True)
        return Response(serializer.data)