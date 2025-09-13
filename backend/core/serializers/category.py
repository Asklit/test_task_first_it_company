from rest_framework import serializers
from ..models import Category, TransactionType


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""

    root_transaction_type = serializers.PrimaryKeyRelatedField(
        queryset=TransactionType.objects.all()
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'root_transaction_type']