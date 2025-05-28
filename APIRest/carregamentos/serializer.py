from rest_framework import serializers
from .models import Carregamento


class CarregamentoSerializer(serializers.ModelSerializer):
    ca_estado_display = serializers.CharField(source='get_ca_estado_display', read_only=True)
    class Meta:
        model = Carregamento
        fields = [
            'id',
            'ca_data_inicio',
            'ca_data_fim',
            'ca_duracao',
            'ca_avg_v',
            'ca_avg_a',
            'ca_avg_kwh',
            'ca_custo',
            'ca_utilizador',
            'ca_Veiculo',
            'ca_posto',
            'ca_entidade',
            'ca_estado',
            'ultimos_dados',
            'ca_estado_display'
        ]