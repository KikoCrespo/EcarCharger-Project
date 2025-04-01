from django.db import models
from entidades.models import Entidade
from utilizadores.models import Utilizador



class Carro(models.Model):
    c_marca = models.CharField(max_length=55)
    c_modelo = models.CharField(max_length=55)
    c_matricula = models.CharField(max_length=55, unique=True)
    c_potencia = models.IntegerField()
    c_ano_e_mes = models.DateField()    
    c_data_registo = models.DateField()                    
    c_categoria = models.IntegerField() #  # 1 - sedan, 2 - SUV, 3 - carrinha, 4 - desportivo, 5 - outro 
    c_estado = models.BooleanField()
    c_img = models.ImageField(max_length=255, blank=True, null=True)
    c_utilizador = models.ManyToManyField(Utilizador, blank=True)
    c_entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Carro' 

    def __str__(self):
        return self.c_matricula


class Anexos(models.Model):
    an_titulo = models.CharField(max_length=100)
    an_data = models.DateField()
    an_anexo = models.ImageField(max_length=255, blank=True, null=True)
    an_carro = models.ForeignKey(Carro, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Anexos'
    
    def __str__(self):
        return self.an_titulo

