from django.db import models
from entidades.models import Entidade
from utilizadores.models import Utilizador
from automoveis.models import Veiculo 
from postosCarregamento.models import PostoCarregamento

# Create your models here.
class Carregamento(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 1),
        ('COMPLETED', 2),
        ('ERROR', 3),
    ]

    ca_data_inicio = models.DateTimeField()
    ca_data_fim = models.DateTimeField(null=True, blank=True)
    ca_duracao = models.IntegerField(null=True, blank=True)
    ca_avg_v = models.FloatField(null=True, blank=True)
    ca_avg_a = models.FloatField(null=True, blank=True)
    ca_avg_kwh = models.FloatField(null=True, blank=True)
    ca_custo = models.FloatField(null=True, blank=True)
    ca_utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    ca_Veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    ca_posto = models.ForeignKey(PostoCarregamento, on_delete=models.CASCADE)
    ca_entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)
    ca_estado = models.IntegerField(choices=STATUS_CHOICES, default=1)
    ultimos_dados = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        db_table = 'Carregamento'
    
    def __str__(self):
        return str(self.ca_data_inicio)
