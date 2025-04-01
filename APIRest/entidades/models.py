from django.db import models

# Create your models here.
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