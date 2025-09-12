import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from transactions.models import TransactionType


@pytest.mark.django_db
class TestTransactionTypeModel:
    """Тесты для модели TransactionType (Тип транзакции)"""
    
    def test_create_transaction_type_success(self):
        """Тест успешного создания типа транзакции"""
        transaction_type = TransactionType.objects.create(name='Пополнение')
        assert transaction_type.name == 'Пополнение'
        assert str(transaction_type) == 'Пополнение'
        assert TransactionType.objects.count() == 1

    def test_transaction_type_unique_name_constraint(self):
        """Тест уникальности названия типа транзакции"""
        TransactionType.objects.create(name='Списание')
        with pytest.raises(IntegrityError):
            TransactionType.objects.create(name='Списание')

    def test_transaction_type_string_representation(self):
        """Тест строкового представления типа транзакции"""
        transaction_type = TransactionType.objects.create(name='Пополнение')
        assert str(transaction_type) == 'Пополнение'

    def test_transaction_type_max_length_validation(self):
        """Тест валидации максимальной длины названия типа транзакции"""
        # Должно пройти - 30 символов
        transaction_type = TransactionType(name='А' * 30)
        transaction_type.full_clean()
        
        # Должно вызвать ошибку - 31 символ
        transaction_type = TransactionType(name='А' * 31)
        with pytest.raises(ValidationError):
            transaction_type.full_clean()

    def test_default_transaction_types_creation(self):
        """Тест создания дефолтных типов транзакций из ТЗ"""
        types = ['Пополнение', 'Списание']
        for type_name in types:
            TransactionType.objects.create(name=type_name)
        
        assert TransactionType.objects.count() == 2
        assert TransactionType.objects.filter(name='Пополнение').exists()
        assert TransactionType.objects.filter(name='Списание').exists()