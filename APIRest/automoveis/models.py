from django.db import models
from entidades.models import Entidade
from utilizadores.models import Utilizador
from uploadFiles import caminho_foto_veiculo, caminho_anexo_veiculo

CATEGORIA_CHOICES = (
    (1, 'Sedan'),
    (2, 'Citadino'),
    (3, 'SUV'),
    (4, 'Comercial'),
    (5, 'Utilitario')
)
ESTADO_CHOICES = (
    (1, 'Disponivel'),
    (2, 'Em Manutencao'),
    (3, 'Avariado'),
    (4, 'Em uso')
)

class Veiculo(models.Model):
    v_modelo = models.CharField(max_length=55, null=True, blank=True)
    v_marca = models.CharField(max_length=55)
    v_cor = models.CharField(max_length=55)
    v_matricula = models.CharField(max_length=55, unique=True)
    v_potencia = models.IntegerField()
    v_data_aquisicao = models.DateField()                 
    v_categoria = models.IntegerField(choices=CATEGORIA_CHOICES) #  1=Sedan, 2=Citadino, 3=SUV, 4=Comercial, 5=Utilitário 
    v_estado = models.IntegerField(choices= ESTADO_CHOICES, default=1) # 1=Disponível, 2=Em Manutenção, 3=Avariado
    v_img = models.ImageField(upload_to=caminho_foto_veiculo,max_length=255, blank=True, null=True)
    v_utilizador = models.ManyToManyField(Utilizador, blank=True)
    v_entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)
    v_assentos = models.IntegerField()
    v_transmissao = models.CharField(max_length=55)
    v_combustivel = models.CharField(max_length=55)
    v_ano_matricula = models.DateField(null=True, blank=True)  # ano de matricula
    v_quilometros = models.IntegerField(null=True, blank=True) # km do veiculo
    v_emissoes = models.IntegerField(null=True, blank=True) # emissao de co2 do veiculo

    class Meta:
        db_table = 'Veiculo' 
        

    def __str__(self):
        return self.v_matricula

TIPO_ANEXO_CHOICES = (
    (1, 'Seguro'),
    (2, 'Inspeção'),
    (3, 'IUC'),
    (4, 'Outros'),
)

class Anexos(models.Model):
    an_tipo = models.IntegerField(choices=TIPO_ANEXO_CHOICES, default=4)
    an_titulo = models.CharField(max_length=100)
    an_data = models.DateField()
    an_data_validade = models.DateField(null=True, blank=True) # fim de vlaidade de um seguro por exemplo
    an_anexo = models.ImageField(upload_to= caminho_anexo_veiculo ,max_length=255, blank=True, null=True)
    an_veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Anexos'
        ordering = ['-an_data']
    
    def __str__(self):
        return self.an_titulo


class Requisicao(models.Model):
    ESTADOS = (
        (1, 'Pendente'),
        (2, 'Aprovada'),
        (3, 'Rejeitada'),
        (4, 'Terminada'),
    )

    r_utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name='requisicoes')
    r_veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='requisicoes')
    r_motivo = models.TextField()
    r_data_inicio = models.DateTimeField()
    r_data_fim = models.DateTimeField(null=True, blank=True)
    r_ilimitado = models.BooleanField(default=False)
    r_estado = models.IntegerField(default=1, choices=ESTADOS)  # 1=Pendente, 2=Aprovada, 3=Rejeitada, 4=Terminada
    r_motivo_terminacao = models.TextField(null=True, blank=True)
    r_entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE, related_name='requisicoes')

    def __str__(self):
        return f"{self.r_utilizador} requisitou {self.r_veiculo}"

    class Meta:
        db_table = 'Requisicao'
        ordering = ['-r_data_inicio']
        unique_together = ('r_utilizador', 'r_veiculo', 'r_data_inicio')
