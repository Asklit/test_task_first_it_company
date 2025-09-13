from django.utils import timezone
from django.db import models
from django.db.models import CASCADE
from django.core.validators import MinValueValidator
from core.services.transaction_validation import validate_transaction

class Transaction(models.Model):
    """
    Entity transaction model
    """
    create_date = models.DateField(
        default=timezone.now, 
    )
    status = models.ForeignKey(
        'Status', 
        on_delete=CASCADE, 
    )
    transaction_type = models.ForeignKey(
        'TransactionType', 
        on_delete=CASCADE, 
    )
    category = models.ForeignKey(
        'Category', 
        on_delete=CASCADE, 
    )
    subcategory = models.ForeignKey(
        'Subcategory', 
        on_delete=CASCADE, 
    )
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
    )
    notes = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
    )

    def clean(self):
        """
        Валидация на уровне модели
        """
        super().clean()
        validate_transaction(self)
    
    def save(self, *args, **kwargs):
        """
        Автоматическая валидация при сохранении
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.create_date} - {self.status.name} - ${self.amount}"
    
    @classmethod
    def get_optimized_queryset(cls):
        """
        Return queryset with select_related
        to avoid N+1 problem
        """
        return cls.objects.select_related(
            'status',
            'transaction_type',
            'category',
            'subcategory'
        )