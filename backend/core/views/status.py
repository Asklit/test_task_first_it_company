from rest_framework import viewsets
from ..models import Status
from ..serializers import StatusSerializer

class StatusViewSet(viewsets.ModelViewSet):

    """CRUD with modelviewset for status"""
    
    queryset = Status.objects.all()
    serializer_class = StatusSerializer