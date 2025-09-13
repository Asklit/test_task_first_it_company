import pytest
from django.contrib.admin.sites import site
from django.urls import reverse
from core.models import Subcategory


@pytest.mark.django_db
class TestSubcategoryAdmin:
    """Тесты для админ-панели Subcategory"""

    def test_subcategory_list_display(self, subcategory):
        """Тест отображения списка подкатегорий в админке"""
        model_admin = site._registry[Subcategory]
        assert model_admin.list_display == ('id', 'name', 'root_category')

    def test_subcategory_list_filter(self, subcategory):
        """Тест фильтров подкатегорий"""
        model_admin = site._registry[Subcategory]
        assert model_admin.list_filter == ('root_category',)

    def test_subcategory_search_fields(self, subcategory):
        """Тест поиска по подкатегориям"""
        model_admin = site._registry[Subcategory]
        assert model_admin.search_fields == ('name',)

    def test_subcategory_admin_changelist(self, admin_client, subcategory):
        """Тест отображения страницы списка подкатегорий"""
        url = reverse('admin:core_subcategory_changelist')
        response = admin_client.get(url)
        assert response.status_code == 200
        assert subcategory.name in str(response.content)

    def test_subcategory_admin_add(self, admin_client, category):
        """Тест добавления подкатегории через админку"""
        url = reverse('admin:core_subcategory_add')
        response = admin_client.get(url)
        assert response.status_code == 200

        data = {
            'name': 'New Subcategory',
            'root_category': category.id
        }
        response = admin_client.post(url, data)
        assert response.status_code == 302
        assert Subcategory.objects.filter(name='New Subcategory').exists()