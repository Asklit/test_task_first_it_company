import pytest
from rest_framework import serializers
from transactions.models import Status
from transactions.serializers import StatusSerializer


@pytest.mark.django_db
class TestStatusSerializer:
    """Тесты для StatusSerializer"""

    def test_serializer_contains_expected_fields(self):
        """Тест на наличие всех полей в сериализаторе"""
        serializer = StatusSerializer()
        fields = set(serializer.fields.keys())
        expected_fields = {'id', 'name'}
        assert fields == expected_fields

    def test_serialize_status_instance(self, status):
        """Тест сериализации существующего статуса"""
        serializer = StatusSerializer(status)
        data = serializer.data

        assert data['id'] == status.id
        assert data['name'] == status.name

    def test_deserialize_valid_data(self):
        """Тест десериализации валидных данных"""
        data = {'name': 'Completed'}
        serializer = StatusSerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data['name'] == 'Completed'

    def test_deserialize_invalid_data(self):
        """Тест десериализации невалидных данных"""
        data = {'name': ''}  # Пустое имя
        serializer = StatusSerializer(data=data)

        assert not serializer.is_valid()
        assert 'name' in serializer.errors

    def test_create_status(self):
        """Тест создания нового статуса"""
        data = {'name': 'Pending'}
        serializer = StatusSerializer(data=data)

        assert serializer.is_valid()
        status_instance = serializer.save()

        assert status_instance.id is not None
        assert status_instance.name == 'Pending'

    def test_update_status(self, status):
        """Тест обновления статуса"""
        data = {'name': 'Updated Status'}
        serializer = StatusSerializer(status, data=data)

        assert serializer.is_valid()
        status_instance = serializer.save()

        assert status_instance.name == 'Updated Status'
        assert status_instance.id == status.id