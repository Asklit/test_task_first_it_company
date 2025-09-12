import pytest
from rest_framework import serializers
from core.models import TransactionType
from core.serializers import TransactionTypeSerializer


@pytest.mark.django_db
class TestTransactionTypeSerializer:
    """Тесты для TransactionTypeSerializer"""

    def test_serializer_contains_expected_fields(self):
        """Тест на наличие всех полей"""
        serializer = TransactionTypeSerializer()
        fields = set(serializer.fields.keys())
        expected_fields = {'id', 'name'}
        assert fields == expected_fields

    def test_deserialize_valid_data(self):
        """Тест десериализации валидных данных"""
        data = {'name': 'Expense'}
        serializer = TransactionTypeSerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data['name'] == 'Expense'

    def test_create_transaction_type(self):
        """Тест создания типа транзакции"""
        data = {'name': 'Income'}
        serializer = TransactionTypeSerializer(data=data)

        assert serializer.is_valid()
        transaction_type = serializer.save()

        assert transaction_type.id is not None
        assert transaction_type.name == 'Income'