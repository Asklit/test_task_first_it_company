import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
class TestSubcategoryFilterView:
    """Тесты для SubcategoryFilterView"""

    def test_filter_subcategories_by_category(self, api_client, subcategory, category):
        """Тест фильтрации подкатегорий по категории"""
        url = reverse('subcategory-filter')
        response = api_client.get(f'{url}?category_id={category.id}')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Monthly'

    def test_get_all_subcategories_without_filter(self, api_client, subcategory):
        """Тест получения всех подкатегорий без фильтра"""
        url = reverse('subcategory-filter')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Monthly'

    def test_filter_subcategories_nonexistent_category(self, api_client):
        """Тест фильтрации подкатегорий по несуществующей категории"""
        url = reverse('subcategory-filter')
        response = api_client.get(f'{url}?category_id=999')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0


@pytest.mark.django_db
class TestCategoryFilterView:
    """Тесты для CategoryFilterView"""

    def test_filter_categories_by_transaction_type(self, api_client, category, transaction_type):
        """Тест фильтрации категорий по типу транзакции"""
        url = reverse('category-filter')
        response = api_client.get(f'{url}?transaction_type_id={transaction_type.id}')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Salary'

    def test_get_all_categories_without_filter(self, api_client, category):
        """Тест получения всех категорий без фильтра"""
        url = reverse('category-filter')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Salary'

    def test_filter_categories_nonexistent_transaction_type(self, api_client):
        """Тест фильтрации категорий по несуществующему типу транзакции"""
        url = reverse('category-filter')
        response = api_client.get(f'{url}?transaction_type_id=999')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0