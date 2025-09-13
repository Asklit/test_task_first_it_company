from django.core.exceptions import ValidationError

def validate_transaction(transaction):
    """
    Валидация транзакции
    """
    errors = {}
    
    # Проверка соответствия категории и типа транзакции
    if (hasattr(transaction, 'category') and 
        hasattr(transaction, 'transaction_type') and
        transaction.category and transaction.transaction_type and
        transaction.category.root_transaction_type != transaction.transaction_type):
        errors['category'] = 'Категория не соответствует типу транзакции'
    
    # Проверка соответствия подкатегории и категории
    if (hasattr(transaction, 'subcategory') and 
        hasattr(transaction, 'category') and
        transaction.subcategory and transaction.category and
        transaction.subcategory.root_category != transaction.category):
        errors['subcategory'] = 'Подкатегория не соответствует категории'
    
    if errors:
        raise ValidationError(errors)