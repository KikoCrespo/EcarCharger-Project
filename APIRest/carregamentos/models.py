from django.db import models
from entidades.models import Entidade
from utilizadores.models import Utilizador
from automoveis.models import Veiculo 
from postosCarregamento.models import PostoCarregamento

# Create your models here.
class Carregamento(models.Model):
    ca_data_inicio = models.DateField()
    ca_data_fim = models.DateField()
    ca_duracao = models.IntegerField()
    ca_avg_v = models.FloatField()
    ca_avg_a = models.FloatField()
    ca_avg_kwh = models.FloatField()
    ca_custo = models.FloatField()
    ca_utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    ca_Veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    ca_posto = models.ForeignKey(PostoCarregamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Carregamento'
    
    def __str__(self):
        return str(self.ca_data_inicio)