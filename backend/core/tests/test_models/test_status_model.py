import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from core.models import Status


@pytest.mark.django_db
class TestStatusModel:
    """Тесты для модели Status (Статус)"""
    
    def test_create_status_success(self):
        """Тест успешного создания статуса"""
        status = Status.objects.create(name='Бизнес')
        assert status.name == 'Бизнес'
        assert str(status) == 'Бизнес'
        assert Status.objects.count() == 1

    def test_status_unique_name_constraint(self):
        """Тест уникальности названия статуса"""
        Status.objects.create(name='Личное')
        with pytest.raises(IntegrityError):
            Status.objects.create(name='Личное')

    def test_status_string_representation(self):
        """Тест строкового представления статуса"""
        status = Status.objects.create(name='Налог')
        assert str(status) == 'Налог'

    def test_status_max_length_validation(self):
        """Тест валидации максимальной длины названия статуса"""
        # Должно пройти - 30 символов
        status = Status(name='А' * 30)
        status.full_clean()  # Не должно вызывать ошибку
        
        # Должно вызвать ошибку - 31 символ
        status = Status(name='А' * 31)
        with pytest.raises(ValidationError):
            status.full_clean()

    def test_default_statuses_creation(self):
        """Тест создания дефолтных статусов из ТЗ"""
        statuses = ['Бизнес', 'Личное', 'Налог']
        for status_name in statuses:
            Status.objects.create(name=status_name)
        
        assert Status.objects.count() == 3
        assert Status.objects.filter(name='Бизнес').exists()
        assert Status.objects.filter(name='Личное').exists()
        assert Status.objects.filter(name='Налог').exists()