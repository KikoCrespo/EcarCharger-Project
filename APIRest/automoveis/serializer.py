from rest_framework import serializers
from .models import Veiculo, Anexos

class VeiculoSerializer(serializers.ModelSerializer):
    v_categoria_display = serializers.CharField(source='get_v_categoria_display', read_only=True)
    class Meta:
        model = Veiculo
        fields = (
            'id', 'v_modelo', 'v_marca', 'v_cor', 'v_matricula', 'v_potencia',
            'v_data_aquisicao', 'v_categoria', 'v_categoria_display', 'v_estado',
            'v_img', 'v_utilizador', 'v_entidade', 'v_assentos', 'v_transmissao',           
            'v_combustivel', 'v_ano_matricula', 'v_quilometros', 'v_emissoes'
        )

class AnexosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexos
        fields = '__all__'