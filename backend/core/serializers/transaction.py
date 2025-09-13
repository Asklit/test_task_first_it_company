from rest_framework import serializers
from django.core.exceptions import ValidationError
from ..models import Transaction, Status, TransactionType, Category, Subcategory
from core.services.transaction_validation import validate_transaction


class TransactionSerializer(serializers.ModelSerializer):
    """Transaction serializer"""

    status = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all()
    )
    transaction_type = serializers.PrimaryKeyRelatedField(
        queryset=TransactionType.objects.all()
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=Subcategory.objects.all()
    )
    notes = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        required=False
    )

    status_name = serializers.CharField(
        source='status.name',
        read_only=True
    )
    transaction_type_name = serializers.CharField(
        source='transaction_type.name',
        read_only=True
    )
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )
    subcategory_name = serializers.CharField(
        source='subcategory.name',
        read_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'create_date',
            'status',
            'status_name',
            'transaction_type',
            'transaction_type_name',
            'category',
            'category_name',
            'subcategory',
            'subcategory_name',
            'amount',
            'notes'
        ]

    @classmethod
    def get_optimized_queryset(cls):
        """
        Return queryset with select_related
        to avoid N+1 problem
        """
        return Transaction.objects.select_related(
            'status',
            'transaction_type',
            'category',
            'subcategory'
        )

    def validate(self, data):
        """
        Validation for category and subcategory

        Subcategory must be related to category
        Category must be related to type
        """
        temp_obj = Transaction(**data)

        try:
            validate_transaction(temp_obj)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return data

    def validate_category(self, value):
        """Validate category matches transaction type"""
        transaction_type = self.initial_data.get('transaction_type')

        if (transaction_type and
                value.root_transaction_type_id != int(transaction_type)):
            raise serializers.ValidationError(
                "Category must be related to transaction type"
            )
        return value

    def validate_subcategory(self, value):
        """Validate subcategory matches category"""
        category = self.initial_data.get('category')

        if category and value.root_category_id != int(category):
            raise serializers.ValidationError(
                "Subcategory must be related to category"
            )
        return value