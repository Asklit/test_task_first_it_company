from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Transaction
from ..serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    
    """CRUD with modelviewset for transaction"""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'create_date': ['exact', 'gte', 'lte'],
        'status': ['exact'],
        'transaction_type': ['exact'],
        'category': ['exact'],
        'subcategory': ['exact'],
    }
    
    def get_queryset(self):
        """Use optimized queryset to avoid N+1 problem"""
        return TransactionSerializer.get_optimized_queryset()