from django.core.exceptions import ValidationError

def validate_transaction(obj):

    """
    Валидация транзакции
    """

    errors = {}
    
    # Проверка положительности суммы
    if obj.amount <= 0:
        errors['amount'] = 'Сумма должна быть положительной.'
    
    # Проверка связи подкатегории с категорией
    if hasattr(obj, 'subcategory') and hasattr(obj, 'category'):
        if obj.subcategory and obj.category and obj.subcategory.root_category != obj.category:
            errors['subcategory'] = 'Подкатегория должна быть выбрана корректно.'
    
    # Проверка связи категории с типом транзакции
    if hasattr(obj, 'category') and hasattr(obj, 'transaction_type'):
        if obj.category and obj.transaction_type and obj.category.root_transaction_type != obj.transaction_type:
            errors['category'] = 'Категория должна соответствовать выбранному типу транзакции.'
    
    if errors:
        raise ValidationError(errors)