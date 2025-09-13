from django.db import models
from django.db.models import CASCADE
from .base import NamedModel

class Subcategory(NamedModel):
    """
    Entity subcategory model
    """
    root_category = models.ForeignKey(
        'Category', 
        on_delete=CASCADE
    )