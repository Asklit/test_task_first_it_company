from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Category
from ..serializers import CategorySerializer

class CategoryFilterView(APIView):
    
    """Filter for category by transaction type"""
    
    def get(self, request):
        transaction_type_id = request.query_params.get('transaction_type_id')
        if transaction_type_id:
            categories = Category.objects.filter(root_transaction_type_id=transaction_type_id)
        else:
            categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)