import pytest
from django.contrib.admin.sites import site
from django.urls import reverse
from transactions.models import Status


@pytest.mark.django_db
class TestStatusAdmin:
    """Тесты для админ-панели Status"""

    def test_status_list_display(self, status):
        """Тест отображения списка статусов в админке"""
        model_admin = site._registry[Status]
        assert model_admin.list_display == ('id', 'name')

    def test_status_search_fields(self, status):
        """Тест поиска по статусам"""
        model_admin = site._registry[Status]
        assert model_admin.search_fields == ('name',)

    def test_status_admin_changelist(self, admin_client, status):
        """Тест отображения страницы списка статусов"""
        url = reverse('admin:transactions_status_changelist')
        response = admin_client.get(url)
        assert response.status_code == 200
        assert status.name in str(response.content)

    def test_status_admin_add(self, admin_client):
        """Тест добавления статуса через админку"""
        url = reverse('admin:transactions_status_add')
        response = admin_client.get(url)
        assert response.status_code == 200

        data = {'name': 'New Status'}
        response = admin_client.post(url, data)
        assert response.status_code == 302
        assert Status.objects.filter(name='New Status').exists()

    def test_status_admin_change(self, admin_client, status):
        """Тест изменения статуса через админку"""
        url = reverse('admin:transactions_status_change', args=[status.id])
        response = admin_client.get(url)
        assert response.status_code == 200

        data = {'name': 'Updated Status'}
        response = admin_client.post(url, data)
        assert response.status_code == 302
        status.refresh_from_db()
        assert status.name == 'Updated Status'