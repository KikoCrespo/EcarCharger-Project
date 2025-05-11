from rest_framework import serializers
from .models import Utilizador

class UtilizadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilizador
        extra_kwargs = {
            'date_joined': {'format': '%Y-%m-%d'},
            'last_login': {'format': '%Y-%m-%d'},
        }
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login']
