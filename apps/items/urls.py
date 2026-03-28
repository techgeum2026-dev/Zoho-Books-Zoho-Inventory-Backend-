"""
URL routing for the Items app.

Uses DRF's DefaultRouter to automatically generate CRUD endpoints for ItemViewSet.
"""
from rest_framework.routers import DefaultRouter

from .views import ItemViewSet

router = DefaultRouter()
router.register(r'', ItemViewSet, basename='item')

urlpatterns = router.urls