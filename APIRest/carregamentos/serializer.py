from rest_framework import serializers
from .models import Carregamento


class CarregamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carregamento
        fields = '__all__'