import pytest
from rest_framework import serializers
from core.models import Subcategory, Category
from core.serializers import SubcategorySerializer


@pytest.mark.django_db
class TestSubcategorySerializer:
    """Тесты для SubcategorySerializer"""

    def test_serializer_contains_expected_fields(self):
        """Тест на наличие всех полей"""
        serializer = SubcategorySerializer()
        fields = set(serializer.fields.keys())
        expected_fields = {'id', 'name', 'root_category'}
        assert fields == expected_fields

    def test_serialize_subcategory_instance(self, subcategory):
        """Тест сериализации подкатегории"""
        serializer = SubcategorySerializer(subcategory)
        data = serializer.data

        assert data['id'] == subcategory.id
        assert data['name'] == subcategory.name
        assert data['root_category'] == subcategory.root_category.id

    def test_deserialize_valid_data(self, category):
        """Тест десериализации валидных данных"""
        data = {
            'name': 'Restaurants',
            'root_category': category.id
        }
        serializer = SubcategorySerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data['name'] == 'Restaurants'
        assert serializer.validated_data['root_category'] == category

    def test_create_subcategory(self, category):
        """Тест создания подкатегории"""
        data = {
            'name': 'Fast Food',
            'root_category': category.id
        }
        serializer = SubcategorySerializer(data=data)

        assert serializer.is_valid()
        subcategory_instance = serializer.save()

        assert subcategory_instance.id is not None
        assert subcategory_instance.name == 'Fast Food'
        assert subcategory_instance.root_category == category

    def test_missing_required_fields(self):
        """Тест отсутствия обязательных полей"""
        data = {'name': 'Test Subcategory'}  # Нет root_category
        serializer = SubcategorySerializer(data=data)

        assert not serializer.is_valid()
        assert 'root_category' in serializer.errors