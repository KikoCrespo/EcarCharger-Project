from django.db import models
from django.contrib.auth.models import AbstractUser
from entidades.models import Entidade
from uploadFiles import caminho_foto_perfil

# your models here.
class Utilizador(AbstractUser):
    u_entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)
    u_tipo = models.IntegerField()
    u_estado = models.BooleanField(default=False)
    u_img_perfil = models.ImageField(upload_to= caminho_foto_perfil, blank=True, null=True)
    u_departamento = models.CharField(max_length=255, blank=True, null=True)

    
    class Meta:
        db_table = 'Utilizador'

    def __str__(self):
        return self.first_name + " " + self.last_name
    