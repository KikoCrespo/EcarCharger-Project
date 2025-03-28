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
from myapi.views import LoginView
from myapi.views import LogoutView
from myapi.views import GetCSRFTokenView
from myapi.views import RegistarView
from myapi.views import RegistarEntidadeView
from myapi.views import LoginEntidadeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('csrf/', GetCSRFTokenView.as_view(), name='csrf_token'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registar/', RegistarView.as_view(), name='registar'),
    path('registarEntidade/', RegistarEntidadeView.as_view(), name='registarEntidade'),
    path('loginEntidade/', LoginEntidadeView.as_view(), name='loginEntidade'),
]
