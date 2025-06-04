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
from django.urls import path ,include
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static




from utilizadores.views import LogoutView
from utilizadores.views import AdminView
#from utilizadores.views import UtilizadorView
from utilizadores.views import LoginUtilizadorView
from utilizadores.views import PerfilUtilizadorView
from utilizadores.views import FuncionarioView, CarregamentosUtilizadorView, DashboardView


from utilizadores.views.AuthView import LogoutView, LoginUtilizadorView
from utilizadores.views.AdminView import AdminView, AlterarUserEstadoView, PromoverUtilizadorView, despromoverUtilizadorView
from utilizadores.views.UserView import PerfilUtilizadorView, FuncionarioView

from automoveis.views.RequisicoesView import requisicaoView, RequisicaoUtilizadorView, RequisicoesVeiculoView
from automoveis.views.VeiculoView import getFrotaEntidade, AddVeiculoEntidadeView, VeiculobyIdView

from entidades.views import RegistarEntidadeView

from carregamentos.views import CarregamentosView


from postosCarregamento.views import PostoCarregamentoView


urlpatterns = [

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh token endpoint
    path("api/admin/", admin.site.urls),
    path('api/login/', LoginUtilizadorView.as_view(), name='loginUtilizador'),
    path('api/logout/', LogoutView, name='logout'),

    path('api/utilizadores/registar/admin/', AdminView.as_view(), name='registar'),
    path('api/utilizadores/registar/utilizador/', FuncionarioView.as_view(), name='registarFuncionario'),
    path('api/utilizadores/editar/', FuncionarioView.as_view(), name='editarUtilizador'),
    path('api/utilizadores/listar/', AdminView.as_view(), name='listarUtilizadores'),
    path('api/utilizadores/estado/<int:user_id>/', AlterarUserEstadoView.as_view(), name='alterarEstado'),
    path('api/utilizadores/promover/<int:user_id>/', PromoverUtilizadorView.as_view(), name='promoverUser'),
    path('api/utilizadores/despromover/<int:user_id>/', despromoverUtilizadorView.as_view(), name='despromoverUser'),


    path('api/frota/adicionar-veiculo/', AddVeiculoEntidadeView.as_view(), name='addVeiculoEntidade'),
    path('api/frota/consultar/', getFrotaEntidade.as_view(), name='Frota'),



    path('api/estatisticas/pessoais/', CarregamentosUtilizadorView.as_view(), name='estatisticasPessoais'),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),

    path('api/carregamentos/iniciar/', CarregamentosView.as_view(), name='carregamentos'),
    #path('api/carregamentos/<int:session_id>/stop/', CarregamentosView.stop_charging_view, name='stop_charging_view'),


    path('api/frota/veiculo/<int:veiculo_id>/', VeiculobyIdView.as_view(), name='VeiculoById'),
    path('api/frota/veiculo/<int:veiculo_id>/requisicoes/', RequisicoesVeiculoView.as_view(), name='requisicoesVeiculo'),
    path('api/frota/requisitar/', requisicaoView.as_view(), name='requisitarVeiculo'),
    path('api/frota/requisicoes/listar/', requisicaoView.as_view(), name='listarRequisicoes'),
    path('api/frota/requisicoes/utilizador/listar/', RequisicaoUtilizadorView.as_view(), name='listarRequisicoeUtilizador'), 
    path('api/frota/requisicoes/alterar_estado/', RequisicaoUtilizadorView.as_view(), name='listarRequisicoeUtilizador'), 

    path('api/carregamentos/iniciar/', CarregamentosView.as_view(), name='carregamentos'),
    path('api/carregamentos/<int:session_id>/stop/', CarregamentosView.stop_charging_view, name='stop_charging_view'),

    path('api/carregamentos/editar/<int:id>/', CarregamentosView.as_view(), name='editarCarregamento'),

    path('api/entidade/postos/adicionar/', PostoCarregamentoView.as_view(), name='adicionarPostoCarregamento'),
    path('api/entidade/postos/listar/', PostoCarregamentoView.as_view(), name='listarPostosCarregamento'),
    path('api/entidades/registar', RegistarEntidadeView.as_view(), name='registarEntidade'),

    path('api/perfil/', PerfilUtilizadorView.as_view(), name='perfil-utilizador'),

]

if settings.DEBUG:  # Só serve os arquivos de mídia durante o desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
