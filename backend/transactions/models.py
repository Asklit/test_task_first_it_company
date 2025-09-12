from tkinter import CASCADE
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from transactions.validation import validate_transaction


class Status(models.Model):
    """Entity status model"""

    name = models.CharField(unique=True, max_length=30)

    def __str__(self):
        return self.name
    
class TransactionType(models.Model):
    """Entity transaction type model"""
    name = models.CharField(unique=True, max_length=30)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    """Entity category model"""
    name = models.CharField(unique=True, max_length=30)
    root_transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    """Entity subcategory model"""
    name = models.CharField(unique=True, max_length=30)
    root_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    """Entity transaction model"""
    create_date = models.DateField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.01)]  )
    notes = models.CharField(max_length=100, blank=True, default=None)

    def clean(self):
        """Валидация на уровне модели"""
        super().clean()
        validate_transaction(self)
    
    def save(self, *args, **kwargs):
        """Автоматическая валидация при сохранении"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.create_date} - {self.status.name} - ${self.amount}"
    