import pytest
from django.contrib.admin.sites import site
from django.urls import reverse
from core.models import TransactionType


@pytest.mark.django_db
class TestTransactionTypeAdmin:
    """Тесты для админ-панели TransactionType"""

    def test_transaction_type_list_display(self, transaction_type):
        """Тест отображения списка типов транзакций в админке"""
        model_admin = site._registry[TransactionType]
        assert model_admin.list_display == ('id', 'name')

    def test_transaction_type_search_fields(self, transaction_type):
        """Тест поиска по типам транзакций"""
        model_admin = site._registry[TransactionType]
        assert model_admin.search_fields == ('name',)

    def test_transaction_type_admin_changelist(self, admin_client, transaction_type):
        """Тест отображения страницы списка типов транзакций"""
        url = reverse('admin:transactions_transactiontype_changelist')
        response = admin_client.get(url)
        assert response.status_code == 200
        assert transaction_type.name in str(response.content)

    def test_transaction_type_admin_add(self, admin_client):
        """Тест добавления типа транзакции через админку"""
        url = reverse('admin:transactions_transactiontype_add')
        response = admin_client.get(url)
        assert response.status_code == 200

        data = {'name': 'New Type'}
        response = admin_client.post(url, data)
        assert response.status_code == 302
        assert TransactionType.objects.filter(name='New Type').exists()