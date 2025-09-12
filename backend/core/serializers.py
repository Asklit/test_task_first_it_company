from tabnanny import verbose
from rest_framework import serializers
from .models import Status, TransactionType, Category, Subcategory, Transaction
from core.validation import validate_transaction
from django.core.exceptions import ValidationError


class StatusSerializer(serializers.ModelSerializer):
    
    """status serializer"""

    class Meta:
        model = Status
        fields = ['id', 'name']


class TransactionTypeSerializer(serializers.ModelSerializer):

    """transaction type serializer"""

    class Meta:
        model = TransactionType
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):

    """categoty serializer"""

    root_transaction_type = serializers.PrimaryKeyRelatedField(queryset=TransactionType.objects.all())

    class Meta:
        model = Category
        fields = ['id', 'name', 'root_transaction_type']


class SubcategorySerializer(serializers.ModelSerializer):

    """subcategoty serializer"""

    root_category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'root_category']


class TransactionSerializer(serializers.ModelSerializer):

    """transaction serializer"""

    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())
    transaction_type = serializers.PrimaryKeyRelatedField(queryset=TransactionType.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=Subcategory.objects.all())
    notes = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    status_name = serializers.CharField(source='status.name', read_only=True)
    transaction_type_name = serializers.CharField(source='transaction_type.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'create_date', 'status', 'status_name', 'transaction_type',
            'transaction_type_name', 'category', 'category_name', 'subcategory',
            'subcategory_name', 'amount', 'notes'
        ]

    def validate(self, data):
        """
        
        Vatidation for category and subcategory

        Subcategoty must related to category
        Categoty must related to type

        """

        temp_obj = Transaction(**data)
        try:
            validate_transaction(temp_obj)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data


class SubcategoryFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name']