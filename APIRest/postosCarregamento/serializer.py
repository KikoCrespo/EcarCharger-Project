from rest_framework import serializers
from .models import PostoCarregamento, IoTEquipamento

class PostoCarregamentotSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostoCarregamento
        fields = '__all__'


class IoTEquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IoTEquipamento
        fields = '__all__'