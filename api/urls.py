from rest_framework.routers import DefaultRouter # Cria automaticamente as rotas para operações da ViewSet
from django.urls import path # Permite criar manualmete as rotas para operações da ViewSet, utilizado para rotas de login e token

from .views import (
    EnvironmentViewSet,
    EquipmentModelViewSet,
    MicrocontrollerViewSet,
    SensorViewSet,
    ReadingViewSet,
    UserViewSet
)
# Importando duas views disponibilizadas pela biblioteca Simple JWT, que é utilizada para trabalhar com autenticação por tokens JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

# Criação da instância router, onde ele organiza automáticamente de rotas
router = DefaultRouter()

router.register('environments', EnvironmentViewSet)
router.register('equipment-models', EquipmentModelViewSet)
router.register('microcontrollers', MicrocontrollerViewSet)
router.register('sensors', SensorViewSet)
router.register('readings', ReadingViewSet)
router.register('users', UserViewSet)

# Variável urlpatterns para identificar os caminhos disponíveis.
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #Quando o usuário fizer uma requisição para /login/, enviando suas credenciais, a biblioteca Simple JWT tentará autenticar o usuário e retornar os tokens.
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Endereço responsável por renovar o Access Token. 
] + router.urls