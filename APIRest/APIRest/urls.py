"""
URL configuration for APIRest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


from utilizadores.views import LogoutView
from utilizadores.views import AdminView
#from utilizadores.views import UtilizadorView
from utilizadores.views import LoginUtilizadorView
from utilizadores.views import PerfilUtilizadorView

from automoveis.views import AddCarroEntidadeView
from automoveis.views import getFrotaEntidade

from entidades.views import RegistarEntidadeView

from carregamentos.views import CarregamentosView

from postosCarregamento.views import PostoCarregamentoView


urlpatterns = [

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh token endpoint
    path("api/admin/", admin.site.urls),
    path('api/login/', LoginUtilizadorView.as_view(), name='loginUtilizador'),
    path('api/logout/', LogoutView, name='logout'),
    path('api/utilizadores/registar/', AdminView.as_view(), name='registar'),
    path('api/utilizadores/editar/', AdminView.as_view(), name='editarUtilizador'),
    path('api/entidades/registar', RegistarEntidadeView.as_view(), name='registarEntidade'),
    path('api/utilizadores/listar/', AdminView.as_view(), name='listarUtilizadores'),
    path('api/registarCarro/', AddCarroEntidadeView.as_view(), name='addCarroEntidade'),
    path('api/Frota/<int:entidade_id>/', getFrotaEntidade.as_view(), name='Frota'),
    path('api/carregamentos/iniciar/', CarregamentosView.as_view(), name='carregamentos'),
    path('api/carregamentos/editar/<int:id>/', CarregamentosView.as_view(), name='editarCarregamento'),
    path('api/entidade/postos/adicionar/', PostoCarregamentoView.as_view(), name='adicionarPostoCarregamento'),
    path('api/entidade/postos/listar/', PostoCarregamentoView.as_view(), name='listarPostosCarregamento'),
    path('api/perfil/', PerfilUtilizadorView.as_view(), name='perfil-utilizador'),
]


