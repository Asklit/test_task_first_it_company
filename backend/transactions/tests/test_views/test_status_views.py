import pytest
from rest_framework import status
from django.urls import reverse
from transactions.models import Status


@pytest.mark.django_db
class TestStatusViewSet:
    """Тесты для StatusViewSet"""

    def test_list_statuses(self, api_client, status):
        """Тест получения списка статусов"""
        url = reverse('status-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Active'

    def test_create_status(self, api_client):
        """Тест создания статуса"""
        url = reverse('status-list')
        data = {'name': 'Completed'}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Status.objects.count() == 1
        assert Status.objects.first().name == 'Completed'

    def test_retrieve_status(self, api_client, status):
        """Тест получения одного статуса"""
        url = reverse('status-detail', kwargs={'pk': status.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Active'

    def test_update_status(slf, api_client, status):
        """Тест обновления статуса"""
        url = reverse('status-detail', kwargs={'pk': status.pk})
        data = {'name': 'Updated'}
        response = api_client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        status.refresh_from_db()
        assert status.name == 'Updated'

    def test_delete_status(self, api_client, status):
        """Тест удаления статуса"""
        url = reverse('status-detail', kwargs={'pk': status.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Status.objects.count() == 0