import pytest
from rest_framework import serializers
from core.models import Category, TransactionType
from core.serializers import CategorySerializer


@pytest.mark.django_db
class TestCategorySerializer:
    """Тесты для CategorySerializer"""

    def test_serializer_contains_expected_fields(self):
        """Тест на наличие всех полей"""
        serializer = CategorySerializer()
        fields = set(serializer.fields.keys())
        expected_fields = {'id', 'name', 'root_transaction_type'}
        assert fields == expected_fields

    def test_serialize_category_instance(self, category):
        """Тест сериализации категории"""
        serializer = CategorySerializer(category)
        data = serializer.data

        assert data['id'] == category.id
        assert data['name'] == category.name
        assert data['root_transaction_type'] == category.root_transaction_type.id

    def test_deserialize_valid_data(self, transaction_type):
        """Тест десериализации валидных данных"""
        data = {
            'name': 'Food',
            'root_transaction_type': transaction_type.id
        }
        serializer = CategorySerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data['name'] == 'Food'
        assert serializer.validated_data['root_transaction_type'] == transaction_type

    def test_create_category(self, transaction_type):
        """Тест создания категории"""
        data = {
            'name': 'Transport',
            'root_transaction_type': transaction_type.id
        }
        serializer = CategorySerializer(data=data)

        assert serializer.is_valid()
        category_instance = serializer.save()

        assert category_instance.id is not None
        assert category_instance.name == 'Transport'
        assert category_instance.root_transaction_type == transaction_type

    def test_missing_required_fields(self):
        """Тест отсутствия обязательных полей"""
        data = {'name': 'Test Category'}  # Нет root_transaction_type
        serializer = CategorySerializer(data=data)

        assert not serializer.is_valid()
        assert 'root_transaction_type' in serializer.errors

    def test_invalid_transaction_type(self):
        """Тест невалидного типа транзакции"""
        data = {
            'name': 'Test Category',
            'root_transaction_type': 999  # Несуществующий ID
        }
        serializer = CategorySerializer(data=data)

        assert not serializer.is_valid()
        assert 'root_transaction_type' in serializer.errors