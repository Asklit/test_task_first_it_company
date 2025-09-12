import pytest
from rest_framework import serializers
from django.core.exceptions import ValidationError
from core.models import Transaction, Status, TransactionType, Category, Subcategory
from core.serializers import TransactionSerializer


@pytest.mark.django_db
class TestTransactionSerializer:
    """Тесты для TransactionSerializer"""

    def test_serializer_contains_expected_fields(self):
        """Тест на наличие всех полей"""
        serializer = TransactionSerializer()
        fields = set(serializer.fields.keys())
        expected_fields = {
            'id', 'create_date', 'status', 'status_name',
            'transaction_type', 'transaction_type_name',
            'category', 'category_name', 'subcategory',
            'subcategory_name', 'amount', 'notes'
        }
        assert fields == expected_fields

    def test_deserialize_valid_data(self, status, transaction_type, category, subcategory):
        """Тест десериализации валидных данных"""
        data = {
            'status': status.id,
            'transaction_type': transaction_type.id,
            'category': category.id,
            'subcategory': subcategory.id,
            'amount': '100',
            'notes': 'Test transaction'
        }
        serializer = TransactionSerializer(data=data)

        assert serializer.is_valid()
        validated_data = serializer.validated_data

        assert validated_data['status'] == status
        assert validated_data['transaction_type'] == transaction_type
        assert validated_data['category'] == category
        assert validated_data['subcategory'] == subcategory
        assert validated_data['amount'] == 100
        assert validated_data['notes'] == 'Test transaction'

    def test_create_transaction(self, status, transaction_type, category, subcategory):
        """Тест создания транзакции"""
        data = {
            'status': status.id,
            'transaction_type': transaction_type.id,
            'category': category.id,
            'subcategory': subcategory.id,
            'amount': '200.75',
            'notes': 'New transaction'
        }
        serializer = TransactionSerializer(data=data)

        assert serializer.is_valid()
        transaction_instance = serializer.save()

        assert transaction_instance.id is not None
        assert transaction_instance.amount == 200.75
        assert transaction_instance.notes == 'New transaction'

    def test_notes_field_blank(self, status, transaction_type, category, subcategory):
        """Тест пустого поля notes"""
        data = {
            'status': status.id,
            'transaction_type': transaction_type.id,
            'category': category.id,
            'subcategory': subcategory.id,
            'amount': '100',
            'notes': ''  # Пустая строка
        }
        serializer = TransactionSerializer(data=data)

        assert serializer.is_valid()
        transaction_instance = serializer.save()

        assert transaction_instance.notes == ''

    def test_missing_required_fields(self):
        """Тест отсутствия обязательных полей"""
        data = {'amount': '100'}  # Только amount
        serializer = TransactionSerializer(data=data)

        assert not serializer.is_valid()
        required_fields = {'status', 'transaction_type', 'category', 'subcategory'}
        for field in required_fields:
            assert field in serializer.errors