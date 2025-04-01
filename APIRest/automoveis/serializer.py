from rest_framework import serializers
from .models import Carro, Anexos
class CarroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carro
        fields = '__all__'

class AnexosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexos
        fields = '__all__'