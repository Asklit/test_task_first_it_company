from rest_framework import serializers
from ..models import Status


class StatusSerializer(serializers.ModelSerializer):
    """Status serializer"""

    class Meta:
        model = Status
        fields = ['id', 'name']