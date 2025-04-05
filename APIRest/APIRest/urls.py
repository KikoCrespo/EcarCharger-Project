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

from utilizadores.views import LogoutView
from utilizadores.views import UtilizadorView
from utilizadores.views import LoginUtilizadorView

from automoveis.views import AddCarroEntidadeView
from automoveis.views import getFrotaEntidade

from entidades.views import RegistarEntidadeView

from carregamentos.views import CarregamentosView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', LoginUtilizadorView.as_view(), name='loginUtilizador'),
    path('logout/', LogoutView, name='logout'),
    path('utilizadores/registar/', UtilizadorView.as_view(), name='registar'),
    path('utilizadores/editar/<int:id>/', UtilizadorView.as_view(), name='editarUtilizador'),
    path('registarEntidade/', RegistarEntidadeView.as_view(), name='registarEntidade'),
    path('utilizadores/listar/', UtilizadorView.as_view(), name='listarUtilizadores'),
    path('registarCarro/', AddCarroEntidadeView.as_view(), name='addCarroEntidade'),
    path('Frota/<int:entidade_id>/', getFrotaEntidade.as_view(), name='Frota'),
    path('carregamentos/iniciar/', CarregamentosView.as_view(), name='carregamentos'),
    path('carregamentos/editar/<int:id>/', CarregamentosView.as_view(), name='editarCarregamento'),
]
