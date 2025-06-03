from rest_framework import serializers
from .models import Utilizador

class UtilizadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilizador
        extra_kwargs = {
            'date_joined': {'format': '%Y-%m-%d'},
            'last_login': {'format': '%Y-%m-%d'},
        }
        u_img_perfil = serializers.ImageField(use_url=True)
        fields = ['id','username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login', 'u_departamento', 'u_img_perfil', 'u_entidade']
