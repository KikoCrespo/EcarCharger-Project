from rest_framework import serializers
from .models import Utilizador

class UtilizadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilizador
        fields = ['username', 'email', 'first_name', 'last_name']
