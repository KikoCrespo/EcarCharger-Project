from django.db import models
from entidades.models import Entidade


# Create your models here.
class PostoCarregamento(models.Model):
    pc_morada = models.CharField(max_length=255)
    pc_data_registo = models.DateField()
    pc_intensidade_a = models.FloatField()
    pc_intensidade_kw = models.FloatField()
    pc_tipo_ligacao = models.IntegerField()
    pc_preco_kwh = models.FloatField()
    pc_estado = models.BooleanField() # alternativa integer - ativo/inativo/manutencao
    pc_img = models.ImageField(max_length=255, blank=True, null=True)
    pc_entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)

    class Meta:
        db_table = 'PostoCarregamento'
    
    def __str__(self):
        return self.pc_morada

class IoTEquipamento(models.Model):
    iot_nome = models.CharField(max_length=55)
    iot_data_registo = models.DateField()
    iot_estado = models.BooleanField(default=False)
    iot_img = models.ImageField(max_length=255, blank=True, null=True)
    iot_posto = models.ForeignKey(PostoCarregamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'IoTEquipamento'
    
    def __str__(self):
        return self.iot_nome