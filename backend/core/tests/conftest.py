# tests/conftest.py
import pytest
from django.utils import timezone
from model_bakery import baker
from core.models import Status, TransactionType, Category, Subcategory, Transaction

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def status():
    return baker.make(Status, name='Active')

@pytest.fixture
def transaction_type():
    return baker.make(TransactionType, name='Income')

@pytest.fixture
def category(transaction_type):
    return baker.make(Category, name='Salary', root_transaction_type=transaction_type)

@pytest.fixture
def subcategory(category):
    return baker.make(Subcategory, name='Monthly', root_category=category)

@pytest.fixture
def transaction(status, transaction_type, category, subcategory):
    return baker.make(
        Transaction,
        status=status,
        transaction_type=transaction_type,
        category=category,
        subcategory=subcategory,
        amount=1000.00,
        create_date=timezone.now().date()
    )

@pytest.fixture
def multiple_statuses():
    return baker.make(Status, _quantity=3)

@pytest.fixture
def multiple_transaction_types():
    return baker.make(TransactionType, _quantity=2)

@pytest.fixture
def multiple_categories(transaction_type):
    return baker.make(Category, root_transaction_type=transaction_type, _quantity=3)

@pytest.fixture
def multiple_subcategories(category):
    return baker.make(Subcategory, root_category=category, _quantity=3)

@pytest.fixture
def multiple_transactions(status, transaction_type, category, subcategory):
    return baker.make(
        Transaction,
        status=status,
        transaction_type=transaction_type,
        category=category,
        subcategory=subcategory,
        amount=1000.00,
        create_date=timezone.now().date(),
        _quantity=5
    )


@pytest.fixture
def admin_client(api_client):
    """Фикстура для клиента администратора"""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='password123'
    )

    api_client.force_login(admin_user)
    return api_client