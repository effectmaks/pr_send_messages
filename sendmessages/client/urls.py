from rest_framework import routers
from .api import ClientsViewSet

router = routers.DefaultRouter()
router.register('clients', ClientsViewSet, basename='clients')
urlpatterns = router.urls
