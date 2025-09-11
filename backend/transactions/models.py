from tkinter import CASCADE
from django.utils import timezone
from django.db import models


class Status(models.Model):
    name = models.CharField(unique=True, max_length=30)

    def __str__(self):
        return self.name
    
class TransactionType(models.Model):
    name = models.CharField(unique=True, max_length=30)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(unique=True, max_length=30)
    root_transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(unique=True, max_length=30)
    root_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    create_date = models.DateField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    notes = models.CharField(max_length=100, blank=True, default=None)

    def __str__(self):
        return self.create_date, self.status, self.amount