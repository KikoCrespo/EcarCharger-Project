from django.db import models
from entidades.models import Entidade
from utilizadores.models import Utilizador


class Veiculo(models.Model):
    v_modelo = models.CharField(max_length=55)
    v_marca = models.CharField(max_length=55)
    v_cor = models.CharField(max_length=55)
    v_matricula = models.CharField(max_length=55, unique=True)
    v_potencia = models.IntegerField()
    v_data_aquisicao = models.DateField()    
    v_data_registo = models.DateField()                    
    v_categoria = models.IntegerField() #  # 1 - sedan, 2 - SUV, 3 - carrinha, 4 - desportivo, 5 - outro 
    v_estado = models.BooleanField()
    v_img = models.ImageField(max_length=255, blank=True, null=True)
    v_utilizador = models.ManyToManyField(Utilizador, blank=True)
    v_entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)
    v_assentos = models.IntegerField()
    v_transmissão = models.CharField(max_length=55)
    v_combustivel = models.CharField(max_length=55)


    class Meta:
        db_table = 'Veiculo' 

    def __str__(self):
        return self.c_matricula


class Anexos(models.Model):
    an_titulo = models.CharField(max_length=100)
    an_data = models.DateField()
    an_anexo = models.ImageField(max_length=255, blank=True, null=True)
    an_veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Anexos'
    
    def __str__(self):
        return self.an_titulo

