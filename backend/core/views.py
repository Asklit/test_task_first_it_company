from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Status, TransactionType, Category, Subcategory, Transaction
from .serializers import (
    StatusSerializer, TransactionTypeSerializer, CategorySerializer,
    SubcategorySerializer, TransactionSerializer, SubcategoryFilterSerializer
)


class StatusViewSet(viewsets.ModelViewSet):

    """CRUD with modelviewset for status"""

    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TransactionTypeViewSet(viewsets.ModelViewSet):

    """CRUD with modelviewset for transaction type"""

    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer


class CategoryViewSet(viewsets.ModelViewSet):

    """CRUD with modelviewset for category"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(viewsets.ModelViewSet):

    """CRUD with modelviewset for subcategory"""

    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class TransactionViewSet(viewsets.ModelViewSet):
    
    """CRUD with modelviewset for transaction"""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]

    # filers 
    filterset_fields = {
        'create_date': ['exact', 'gte', 'lte'],
        'status': ['exact'],
        'transaction_type': ['exact'],
        'category': ['exact'],
        'subcategory': ['exact'],
    }


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


class CategoryFilterView(APIView):
    """Filter for subcategory"""
    def get(self, request):
        transaction_type_id = request.query_params.get('transaction_type_id')
        if transaction_type_id:
            categories = Category.objects.filter(root_transaction_type_id=transaction_type_id)
        else:
            categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)