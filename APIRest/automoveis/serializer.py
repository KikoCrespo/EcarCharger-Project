from rest_framework import serializers
from .models import Veiculo, Anexos, Requisicao
from utilizadores.serializer import UtilizadorSerializer

class VeiculoSerializer(serializers.ModelSerializer):
    v_categoria_display = serializers.CharField(source='get_v_categoria_display', read_only=True) # Display the category choice 
    v_estado_display = serializers.CharField(source='get_v_estado_display', read_only=True) # Display the state choice
    v_img = serializers.ImageField(use_url=True) 
    v_ano = serializers.DateField(source='v_ano_matricula', format="%Y", read_only=True)  
    v_mes_matricula = serializers.DateField(source='v_ano_matricula', format="%m", read_only=True)
    v_ano_mes_matricula = serializers.DateField(source='v_ano_matricula', format="%Y-%m", read_only=True)  # Assuming v_ano_matricula is a DateField
    class Meta:
        model = Veiculo
        fields = (
            'id', 'v_modelo', 'v_marca', 'v_cor', 'v_matricula', 'v_potencia',
            'v_data_aquisicao', 'v_categoria', 'v_categoria_display', 'v_estado',
            'v_img', 'v_utilizador', 'v_entidade', 'v_assentos', 'v_transmissao',           
            'v_combustivel', 'v_quilometros', 'v_emissoes', 'v_estado_display', 'v_ano_mes_matricula', 'v_mes_matricula', 'v_ano'
        )

class AnexosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexos
        fields = '__all__'


class RequisicaoSerializer(serializers.ModelSerializer):
    r_estado_display = serializers.CharField(source='get_r_estado_display', read_only=True)  # Display the state choice
    r_utilizador = UtilizadorSerializer(read_only=True)
    r_veiculo = VeiculoSerializer(read_only=True)
    r_data_inicio = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    r_data_fim = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Requisicao
        fields = [ 
            'id', 'r_data_inicio', 'r_data_fim', 'r_estado', 'r_veiculo',
            'r_utilizador', 'r_entidade', 'r_motivo','r_estado_display', 'r_ilimitado', 'r_motivo_terminacao'
        ]