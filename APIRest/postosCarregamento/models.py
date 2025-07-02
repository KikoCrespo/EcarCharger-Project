from django.db import models
from entidades.models import Entidade


# Create your models here.
class IoTEquipamento(models.Model):
    iot_nome = models.CharField(max_length=55)
    iot_data_registo = models.DateField()
    iot_estado = models.BooleanField(default=False) #ok, em manutenção, avariado
    iot_img = models.ImageField(max_length=255, blank=True, null=True)
    iot_url = models.CharField(max_length=255)
    iot_output = models.IntegerField() #



    class Meta:
        db_table = 'IoTEquipamento'

    def __str__(self):
        return self.iot_nome

class Iot_Entidade(models.Model):
    iot_equipamento = models.ForeignKey(IoTEquipamento, on_delete=models.CASCADE)
    entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Iot_Entidade'
        unique_together = ('iot_equipamento', 'entidade')

    def __str__(self):
        return f"{self.iot_equipamento} ↔ {self.entidade}"

class PostoCarregamento(models.Model):
    pc_morada = models.CharField(max_length=255)
    pc_data_registo = models.DateField()
    pc_intensidade_a = models.FloatField()
    pc_potencia_kw = models.FloatField()
    pc_tipo_ligacao = models.IntegerField()
    pc_preco_kwh = models.FloatField()
    pc_estado = models.BooleanField() # (disponivel,em uso) alternativa integer - ativo/inativo/manutencao
    pc_img = models.ImageField(max_length=255, blank=True, null=True)
    pc_entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)
    pc_iot_equipamento = models.ForeignKey(IoTEquipamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'PostoCarregamento'

    def getPostosCarregamento(self):
        return PostoCarregamento.objects.filter(pc_entidade=self.pc_entidade)

    
    def __str__(self):
        return self.pc_morada



