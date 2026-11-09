from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    EnvironmentViewSet,
    EquipmentModelViewSet,
    MicrocontrollerViewSet,
    SensorViewSet,
    ReadingViewSet,
    UserViewSet
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

router = DefaultRouter()

router.register('environments', EnvironmentViewSet)
router.register('equipment-models', EquipmentModelViewSet)
router.register('microcontrollers', MicrocontrollerViewSet)
router.register('sensors', SensorViewSet)
router.register('readings', ReadingViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls