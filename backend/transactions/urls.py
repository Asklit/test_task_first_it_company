from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StatusViewSet, TransactionTypeViewSet, CategoryViewSet,
    SubcategoryViewSet, TransactionViewSet, SubcategoryFilterView, CategoryFilterView
)

router = DefaultRouter()
router.register(r'statuses', StatusViewSet)
router.register(r'transaction-types', TransactionTypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('subcategories/filter/', SubcategoryFilterView.as_view(), name='subcategory-filter'),
    path('categories/filter/', CategoryFilterView.as_view(), name='category-filter'),
]