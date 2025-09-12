import pytest
from rest_framework import serializers
from core.models import Subcategory
from core.serializers import SubcategoryFilterSerializer


@pytest.mark.django_db
class TestSubcategoryFilterSerializer:
    """Тесты для SubcategoryFilterSerializer"""

    def test_serializer_contains_expected_fields(self):
        """Тест на наличие всех полей"""
        serializer = SubcategoryFilterSerializer()
        fields = set(serializer.fields.keys())
        expected_fields = {'id', 'name'}
        assert fields == expected_fields

    def test_serialize_subcategory_instance(self, subcategory):
        """Тест сериализации подкатегории"""
        serializer = SubcategoryFilterSerializer(subcategory)
        data = serializer.data

        assert data['id'] == subcategory.id
        assert data['name'] == subcategory.name