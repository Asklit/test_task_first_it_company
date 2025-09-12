import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date
from decimal import Decimal
from core.models import Transaction, Status, TransactionType, Category, Subcategory


@pytest.mark.django_db
class TestTransactionModel:
    """Тесты для модели Transaction (Транзакция)"""
    
    def test_create_transaction_success(self, status, transaction_type, category, subcategory):
        """Тест успешного создания транзакции"""
        transaction = Transaction.objects.create(
            create_date=date(2025, 1, 1),
            status=status,
            transaction_type=transaction_type,
            category=category,
            subcategory=subcategory,
            amount=Decimal('1000.00'),
            notes='Тестовый комментарий'
        )
        
        assert transaction.amount == Decimal('1000.00')
        assert transaction.status == status
        assert transaction.transaction_type == transaction_type
        assert transaction.category == category
        assert transaction.subcategory == subcategory
        assert transaction.notes == 'Тестовый комментарий'
        assert Transaction.objects.count() == 1

    def test_transaction_negative_amount_validation(self, status, transaction_type, category, subcategory):
        """Тест валидации отрицательной суммы"""
        transaction = Transaction(
            status=status,
            transaction_type=transaction_type,
            category=category,
            subcategory=subcategory,
            amount=Decimal('-100.00')  # Отрицательная сумма
        )
        
        with pytest.raises(ValidationError) as exc_info:
            transaction.full_clean()
        assert 'amount' in exc_info.value.error_dict

    def test_transaction_zero_amount_validation(self, status, transaction_type, category, subcategory):
        """Тест валидации нулевой суммы"""
        transaction = Transaction(
            status=status,
            transaction_type=transaction_type,
            category=category,
            subcategory=subcategory,
            amount=Decimal('0.00')  # Нулевая сумма
        )
        
        with pytest.raises(ValidationError) as exc_info:
            transaction.full_clean()
        assert 'amount' in exc_info.value.error_dict

    def test_transaction_max_digits_validation(self, status, transaction_type, category, subcategory):
        """Тест валидации максимального количества цифр"""
        # Должно пройти - 15 цифр, 2 знака после запятой
        transaction = Transaction(
            status=status,
            transaction_type=transaction_type,
            category=category,
            subcategory=subcategory,
            amount=Decimal('9999999999999.99')  # 13 цифр + 2 знака
        )
        transaction.full_clean()
        
        # Должно вызвать ошибку - слишком большое число
        transaction.amount = Decimal('100000000000000.00')  # 15 цифр
        with pytest.raises(ValidationError):
            transaction.full_clean()

    def test_transaction_notes_max_length_validation(self, status, transaction_type, category, subcategory):
        """Тест валидации максимальной длины комментария"""
        # Должно пройти - 100 символов
        transaction = Transaction(
            status=status,
            transaction_type=transaction_type,
            category=category,
            subcategory=subcategory,
            amount=Decimal('100.00'),
            notes='А' * 100
        )
        transaction.full_clean()
        
        # Должно вызвать ошибку - 101 символ
        transaction.notes = 'А' * 101
        with pytest.raises(ValidationError):
            transaction.full_clean()