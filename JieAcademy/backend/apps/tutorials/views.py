from rest_framework import viewsets, permissions
from .models import UserContribution
from .serializers import UserContributionSerializer

class UserContributionViewSet(viewsets.ModelViewSet):
    serializer_class = UserContributionSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = UserContribution.objects.select_related('user').all()
        target_id = self.request.query_params.get('target_id', None)
        target_type = self.request.query_params.get('target_type', None)
        category = self.request.query_params.get('category', None)
        
        if target_id:
            queryset = queryset.filter(target_id=target_id)
        if target_type:
            queryset = queryset.filter(target_type=target_type)
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
