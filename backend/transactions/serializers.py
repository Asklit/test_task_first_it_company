from tabnanny import verbose
from rest_framework import serializers
from .models import Status, TransactionType, Category, Subcategory, Transaction


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    root_transaction_type = serializers.PrimaryKeyRelatedField(queryset=TransactionType.objects.all())

    class Meta:
        model = Category
        fields = ['id', 'name', 'root_transaction_type']


class SubcategorySerializer(serializers.ModelSerializer):
    root_category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'root_category']


class TransactionSerializer(serializers.ModelSerializer):
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
        subcategory = data.get('subcategory')
        category = data.get('category')
        if subcategory and category and subcategory.root_category != category:
            raise serializers.ValidationError(
                {"subcategory": "Подкатегория должна быть выбрана корректно."}
            )
        transaction_type = data.get('transaction_type')
        if category and transaction_type and category.root_transaction_type != transaction_type:
            raise serializers.ValidationError(
                {"category": "Категория должна соответствовать выбранному типу транзакции."}
            )

        return data


class SubcategoryFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name']