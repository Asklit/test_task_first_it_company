import pytest
from django.contrib.admin.sites import site
from django.urls import reverse
from transactions.models import Category


@pytest.mark.django_db
class TestCategoryAdmin:
    """Тесты для админ-панели Category"""

    def test_category_list_display(self, category):
        """Тест отображения списка категорий в админке"""
        model_admin = site._registry[Category]
        assert model_admin.list_display == ('id', 'name', 'root_transaction_type')

    def test_category_list_filter(self, category):
        """Тест фильтров категорий"""
        model_admin = site._registry[Category]
        assert model_admin.list_filter == ('root_transaction_type',)

    def test_category_search_fields(self, category):
        """Тест поиска по категориям"""
        model_admin = site._registry[Category]
        assert model_admin.search_fields == ('name',)

    def test_category_admin_changelist(self, admin_client, category):
        """Тест отображения страницы списка категорий"""
        url = reverse('admin:transactions_category_changelist')
        response = admin_client.get(url)
        assert response.status_code == 200
        assert category.name in str(response.content)

    def test_category_admin_add(self, admin_client, transaction_type):
        """Тест добавления категории через админку"""
        url = reverse('admin:transactions_category_add')
        response = admin_client.get(url)
        assert response.status_code == 200

        data = {
            'name': 'New Category',
            'root_transaction_type': transaction_type.id
        }
        response = admin_client.post(url, data)
        assert response.status_code == 302
        assert Category.objects.filter(name='New Category').exists()