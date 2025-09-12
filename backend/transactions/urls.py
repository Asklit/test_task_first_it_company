from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StatusViewSet, TransactionTypeViewSet, CategoryViewSet,
    SubcategoryViewSet, TransactionViewSet, SubcategoryFilterView, CategoryFilterView
)

"""endpoints for frontend"""

router = DefaultRouter()
router.register(r'status', StatusViewSet, basename='status')
router.register(r'transaction-type', TransactionTypeViewSet, basename='transactiontype')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'subcategory', SubcategoryViewSet, basename='subcategory')
router.register(r'transaction', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),  # Убрали лишний /api/
    path('subcategory-filter/', SubcategoryFilterView.as_view(), name='subcategory-filter'),
    path('category-filter/', CategoryFilterView.as_view(), name='category-filter'),
]