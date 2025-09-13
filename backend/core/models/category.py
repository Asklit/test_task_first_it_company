from django.db import models
from django.db.models import CASCADE
from .base import NamedModel

class Category(NamedModel):
    """
    Entity category model
    """
    root_transaction_type = models.ForeignKey(
        'TransactionType', 
        on_delete=CASCADE
    )