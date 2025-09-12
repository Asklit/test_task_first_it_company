import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from transactions.models import Subcategory, Category, TransactionType


@pytest.mark.django_db
class TestSubcategoryModel:
    """Тесты для модели Subcategory (Подкатегория)"""
    
    def test_create_subcategory_success(self, category):
        """Тест успешного создания подкатегории"""
        subcategory = Subcategory.objects.create(
            name='VPS',
            root_category=category
        )
        assert subcategory.name == 'VPS'
        assert subcategory.root_category == category
        assert str(subcategory) == 'VPS'
        assert Subcategory.objects.count() == 1

    def test_subcategory_unique_name_constraint(self, category):
        """Тест уникальности названия подкатегории"""
        Subcategory.objects.create(name='Proxy', root_category=category)
        with pytest.raises(IntegrityError):
            Subcategory.objects.create(name='Proxy', root_category=category)

    def test_subcategory_string_representation(self, category):
        """Тест строкового представления подкатегории"""
        subcategory = Subcategory.objects.create(name='VPS', root_category=category)
        assert str(subcategory) == 'VPS'

    def test_subcategory_max_length_validation(self, category):
        """Тест валидации максимальной длины названия подкатегории"""
        # Должно пройти - 30 символов
        subcategory = Subcategory(name='А' * 30, root_category=category)
        subcategory.full_clean()
        
        # Должно вызвать ошибку - 31 символ
        subcategory = Subcategory(name='А' * 31, root_category=category)
        with pytest.raises(ValidationError):
            subcategory.full_clean()

    def test_subcategory_cascade_delete_category(self, category):
        """Тест каскадного удаления при удалении категории"""
        subcategory = Subcategory.objects.create(name='VPS', root_category=category)
        
        category_id = category.id
        category.delete()
        
        # Подкатегория должна быть удалена каскадно
        assert not Subcategory.objects.filter(id=subcategory.id).exists()

    def test_default_subcategories_creation(self, category):
        """Тест создания дефолтных подкатегорий из ТЗ"""
        subcategories = ['VPS', 'Proxy', 'Farpost', 'Avito']
        for subcategory_name in subcategories:
            Subcategory.objects.create(name=subcategory_name, root_category=category)
        
        assert Subcategory.objects.count() == 4
        assert Subcategory.objects.filter(name='VPS').exists()
        assert Subcategory.objects.filter(name='Proxy').exists()
        assert Subcategory.objects.filter(name='Farpost').exists()
        assert Subcategory.objects.filter(name='Avito').exists()