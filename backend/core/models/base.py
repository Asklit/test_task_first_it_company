from django.db import models


class NamedModel(models.Model):
    """
    Base abstract model with name и __str__ dunder method
    """
    name = models.CharField(unique=True, max_length=30)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name