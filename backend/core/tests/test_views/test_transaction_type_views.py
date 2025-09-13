import pytest
from rest_framework import status
from django.urls import reverse
from core.models import TransactionType

@pytest.mark.django_db
class TestTransactionTypeViewSet:
    """Тесты для TransactionTypeViewSet"""

    def test_list_transaction_types(self, api_client, transaction_type):
        """Тест получения списка типов транзакций"""
        url = reverse('transactiontype-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == 'Income'
        

    def test_create_transaction_type(self, api_client):
        """Тест создания типа транзакции"""
        url = reverse('transactiontype-list')
        data = {'name': 'Expense'}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert TransactionType.objects.count() == 1
        assert TransactionType.objects.first().name == 'Expense'

    def test_retrieve_transaction_type(self, api_client, transaction_type):
        """Тест получения одного типа транзакции"""
        url = reverse('transactiontype-detail', kwargs={'pk': transaction_type.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Income'

    def test_update_transaction_type(self, api_client, transaction_type):
        """Тест обновления типа транзакции"""
        url = reverse('transactiontype-detail', kwargs={'pk': transaction_type.pk})
        data = {'name': 'Transfer'}
        response = api_client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        transaction_type.refresh_from_db()
        assert transaction_type.name == 'Transfer'

    def test_delete_transaction_type(self, api_client, transaction_type):
        """Тест удаления типа транзакции"""
        url = reverse('transactiontype-detail', kwargs={'pk': transaction_type.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert TransactionType.objects.count() == 0