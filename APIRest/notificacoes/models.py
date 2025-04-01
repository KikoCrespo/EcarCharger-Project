from django.db import models
from entidades.models import Entidade
from utilizadores.models import Utilizador
from carregamentos.models import Carregamento

# Create your models here.
class Notificacoes(models.Model):
    nt_data = models.DateField()
    nt_titulo = models.CharField(max_length=255)
    nt_mensagem = models.TextField()
    nt_estado = models.BooleanField(default=False)
    nt_tipo = models.IntegerField()
    nt_utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    nt_entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)
    nt_carregamento = models.ForeignKey(Carregamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Notificacoes'
        ordering = ['nt_data']
    
    def __str__(self):
        return self.nt_titulo
