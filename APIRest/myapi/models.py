from django.db import models

class Entidade(models.Model):
    e_nome = models.CharField(max_length=255)
    e_email = models.EmailField(unique=True)
    e_nif = models.CharField(max_length=255)
    e_contacto = models.CharField(max_length=255)
    e_morada = models.CharField(max_length=255)    
    e_ordem = models.CharField(max_length=255)                     
    e_data_registo = models.DateField()

    class Meta:
        db_table = 'Entidade' 

    def __str__(self):
        return self.e_nome

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

class Carro(models.Model):
    c_marca = models.CharField(max_length=55)
    c_modelo = models.CharField(max_length=55)
    c_matricula = models.CharField(max_length=55)
    c_potencia = models.IntegerField()
    c_ano_e_mes = models.DateField()    
    c_data_registo = models.DateField()                    
    c_categoria = models.IntegerField()
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

class PostoCarregamento(models.Model):
    pc_morada = models.CharField(max_length=255)
    pc_data_registo = models.DateField()
    pc_intensidade_a = models.FloatField()
    pc_intensidade_kw = models.FloatField()
    pc_tipo_ligacao = models.IntegerField()
    pc_preco_kwh = models.FloatField()
    pc_estado = models.BooleanField()
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

class Carregamento(models.Model):
    ca_data_inicio = models.DateField()
    ca_data_fim = models.DateField()
    ca_duracao = models.IntegerField()
    ca_avg_v = models.FloatField()
    ca_avg_a = models.FloatField()
    ca_avg_kwh = models.FloatField()
    ca_custo = models.FloatField()
    ca_utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    ca_carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    ca_posto = models.ForeignKey(PostoCarregamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Carregamento'
    
    def __str__(self):
        return str(self.ca_data_inicio)

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

