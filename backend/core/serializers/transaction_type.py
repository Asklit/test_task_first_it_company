from rest_framework import serializers
from ..models import TransactionType


class TransactionTypeSerializer(serializers.ModelSerializer):
    """Transaction type serializer"""

    class Meta:
        model = TransactionType
        fields = ['id', 'name']