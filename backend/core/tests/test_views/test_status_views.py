import pytest
from rest_framework import status
from django.urls import reverse
from core.models import Status


@pytest.mark.django_db
class TestStatusViewSet:
    """Тесты для StatusViewSet"""
    def test_create_status(self, api_client):
        """Тест создания статуса"""
        url = reverse('status-list')
        data = {'name': 'Completed'}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Status.objects.count() == 1
        assert Status.objects.first().name == 'Completed'