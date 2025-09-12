import pytest
from rest_framework import status
from django.urls import reverse
from core.models import Category


@pytest.mark.django_db
class TestCategoryViewSet:
    """Тесты для CategoryViewSet"""

    def test_list_categories(self, api_client, category):
        """Тест получения списка категорий"""
        url = reverse('category-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Salary'

    def test_create_category(self, api_client, transaction_type):
        """Тест создания категории"""
        url = reverse('category-list')
        data = {'name': 'Food', 'root_transaction_type': transaction_type.id}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.count() == 1
        assert Category.objects.first().name == 'Food'

    def test_retrieve_category(self, api_client, category):
        """Тест получения одной категории"""
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Salary'

    def test_update_category(self, api_client, category, transaction_type):
        """Тест обновления категории"""
        url = reverse('category-detail', kwargs={'pk': category.pk})
        data = {'name': 'Updated Category', 'root_transaction_type': transaction_type.id}
        response = api_client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        category.refresh_from_db()
        assert category.name == 'Updated Category'

    def test_delete_category(self, api_client, category):
        """Тест удаления категории"""
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Category.objects.count() == 0