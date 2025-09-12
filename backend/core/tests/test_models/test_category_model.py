import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from core.models import Category, TransactionType


@pytest.mark.django_db
class TestCategoryModel:
    """Тесты для модели Category (Категория)"""
    
    def test_create_category_success(self, transaction_type):
        """Тест успешного создания категории"""
        category = Category.objects.create(
            name='Инфраструктура',
            root_transaction_type=transaction_type
        )
        assert category.name == 'Инфраструктура'
        assert category.root_transaction_type == transaction_type
        assert str(category) == 'Инфраструктура'
        assert Category.objects.count() == 1

    def test_category_unique_name_constraint(self, transaction_type):
        """Тест уникальности названия категории"""
        Category.objects.create(name='Маркетинг', root_transaction_type=transaction_type)
        with pytest.raises(IntegrityError):
            Category.objects.create(name='Маркетинг', root_transaction_type=transaction_type)

    def test_category_string_representation(self, transaction_type):
        """Тест строкового представления категории"""
        category = Category.objects.create(
            name='Инфраструктура', 
            root_transaction_type=transaction_type
        )
        assert str(category) == 'Инфраструктура'

    def test_category_max_length_validation(self, transaction_type):
        """Тест валидации максимальной длины названия категории"""
        # Должно пройти - 30 символов
        category = Category(name='А' * 30, root_transaction_type=transaction_type)
        category.full_clean()
        
        # Должно вызвать ошибку - 31 символ
        category = Category(name='А' * 31, root_transaction_type=transaction_type)
        with pytest.raises(ValidationError):
            category.full_clean()

    def test_category_cascade_delete_transaction_type(self):
        """Тест каскадного удаления при удалении типа транзакции"""
        transaction_type = TransactionType.objects.create(name='Тестовый тип')
        category = Category.objects.create(
            name='Тестовая категория',
            root_transaction_type=transaction_type
        )
        
        transaction_type_id = transaction_type.id
        transaction_type.delete()
        
        # Категория должна быть удалена каскадно
        assert not Category.objects.filter(id=category.id).exists()

    def test_default_categories_creation(self, transaction_type):
        """Тест создания дефолтных категорий из ТЗ"""
        categories = ['Инфраструктура', 'Маркетинг']
        for category_name in categories:
            Category.objects.create(name=category_name, root_transaction_type=transaction_type)
        
        assert Category.objects.count() == 2
        assert Category.objects.filter(name='Инфраструктура').exists()
        assert Category.objects.filter(name='Маркетинг').exists()