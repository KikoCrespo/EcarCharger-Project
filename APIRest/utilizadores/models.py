from django.db import models
from entidades.models import Entidade

# Create your models here.
class Utilizador(models.Model):
    u_nome = models.CharField(max_length=55)
    u_password = models.CharField(max_length=255)
    u_email = models.EmailField(unique=True)
    u_entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)
    u_data_registo = models.DateField()
    u_tipo = models.IntegerField()
    u_estado = models.BooleanField(default=False)
    u_token = models.CharField(max_length=255, blank=True, null=True)
    u_img_perfil = models.ImageField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Utilizador'
    
    def __str__(self):
        return self.u_nome