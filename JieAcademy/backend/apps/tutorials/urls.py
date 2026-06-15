from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserContributionViewSet

router = DefaultRouter()
router.register(r'contributions', UserContributionViewSet, basename='contribution')

urlpatterns = [
    path('', include(router.urls)),
]
