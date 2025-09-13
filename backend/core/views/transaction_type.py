from rest_framework import viewsets
from ..models import TransactionType
from ..serializers import TransactionTypeSerializer

class TransactionTypeViewSet(viewsets.ModelViewSet):

    """CRUD with modelviewset for transaction type"""
    
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer