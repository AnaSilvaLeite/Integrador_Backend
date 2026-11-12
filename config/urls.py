from django.contrib import admin # Permite acessar o painel administrativo, onde podemos gerenciar registros e dados cadastrados no banco de dados
from django.urls import path, include # Include - permite incluir as rotas de outro arquivo dentro do arquivo atual.
from django.conf import settings # Importa as configurações gerais do projeto, que ficam em settings
from django.conf.urls.static import static # Utilizada para disponibilizar arquivos de mídia

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # include('api.urls') - informa ao Django que ele deve procurar as demais rotas dentro do arquivo api/urls.py
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)