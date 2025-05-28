from django.db import models
from django.contrib.auth.models import AbstractUser
from entidades.models import Entidade
from uploadFiles import caminho_foto_perfil
from datetime import timedelta
from django.utils import timezone

class Utilizador(AbstractUser):
    u_entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)
    u_tipo = models.IntegerField()
    u_estado = models.BooleanField(default=False)
    u_img_perfil = models.ImageField(upload_to=caminho_foto_perfil, blank=True, null=True)
    u_departamento = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Utilizador'

    def getCarregamentos(self):
        from carregamentos.models import Carregamento
        return Carregamento.objects.filter(ca_utilizador=self)

    def getNrCarregamentos(self):
        from carregamentos.models import Carregamento
        carregamentos_now = Carregamento.objects.filter(ca_utilizador=self).count()

        return carregamentos_now, carregamentos_semana, carregamentos_mes

    def calcular_totais(self):
        from carregamentos.models import Carregamento  # Importa o modelo Carregamento

        # Obtém os carregamentos do utilizador
        carregamentos = self.getCarregamentos()

        # Totais mensais
        #Nr carregamentos
        total_carregamentos_mensal = carregamentos.filter(ca_data_inicio__month=timezone.now().month,
                                                          ca_data_inicio__year=timezone.now().year).count()
        # Nr carregamentos do mês anterior
        total_carregamentos_mensal_before = Carregamento.objects.filter(ca_utilizador=self, ca_data_inicio__year=timezone.now().year, ca_data_inicio__month=timezone.now().month - 1).count()

        # Quantidade total de kWh carregados
        total_quantidade_mensal = sum(carregamento.ca_avg_kwh for carregamento in carregamentos
                                      if carregamento.ca_data_inicio.month == timezone.now().month and
                                      carregamento.ca_data_inicio.year == timezone.now().year)
        # Quantidade total de kWh carregados do mês anterior
        total_quantidade_mensal_before = sum(carregamento.ca_avg_kwh for carregamento in carregamentos
                                                    if carregamento.ca_data_inicio.month == timezone.now().month - 1 and
                                                    carregamento.ca_data_inicio.year == timezone.now().year)
        # Custo total dos carregamentos
        total_custo_mensal = sum(carregamento.ca_custo for carregamento in carregamentos
                                 if carregamento.ca_data_inicio.month == timezone.now().month and
                                 carregamento.ca_data_inicio.year == timezone.now().year)
        # Custo total dos carregamentos do mês anterior
        total_custo_mensal_before = sum(carregamento.ca_custo for carregamento in carregamentos
                                                if carregamento.ca_data_inicio.month == timezone.now().month - 1 and
                                                carregamento.ca_data_inicio.year == timezone.now().year)

        # Totais semanais
        start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
        total_carregamentos_semanal = carregamentos.filter(ca_data_inicio__gte=start_of_week).count()
        total_carregamentos_semanal_before= Carregamento.objects.filter(ca_utilizador=self, ca_data_inicio__lt=timezone.now() - timedelta(days=7)).count()

        total_quantidade_semanal = sum(carregamento.ca_avg_kwh for carregamento in carregamentos
                                       if carregamento.ca_data_inicio >= start_of_week)
        total_quantidade_semanal_before = sum(carregamento.ca_avg_kwh for carregamento in carregamentos
                                                  if carregamento.ca_data_inicio < start_of_week and
                                                    carregamento.ca_data_inicio >= start_of_week - timedelta(days=7))

        total_custo_semanal = sum(carregamento.ca_custo for carregamento in carregamentos
                                  if carregamento.ca_data_inicio >= start_of_week)
        total_custo_semanal_before = sum(carregamento.ca_custo for carregamento in carregamentos
                                            if carregamento.ca_data_inicio < start_of_week and
                                            carregamento.ca_data_inicio >= start_of_week - timedelta(days=7))




        return {
            'total_carregamentos_mensal': total_carregamentos_mensal,
            'total_carregamentos_mensal_before': total_carregamentos_mensal_before,
            'total_quantidade_mensal': total_quantidade_mensal,
            'total_quantidade_mensal_before': total_quantidade_mensal_before,
            'total_custo_mensal': total_custo_mensal,
            'total_custo_mensal_before': total_custo_mensal_before,
            'total_carregamentos_semanal': total_carregamentos_semanal,
            'total_carregamentos_semanal_before': total_carregamentos_semanal_before,
            'total_quantidade_semanal': total_quantidade_semanal,
            'total_quantidade_semanal_before': total_quantidade_semanal_before,
            'total_custo_semanal': total_custo_semanal,
            'total_custo_semanal_before': total_custo_semanal_before,
        }


    def calcular_custos_totais_semanais(self):
        from carregamentos.models import Carregamento

        carregamentos = self.getCarregamentos()
        start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())

        custos_diarios_now = {
            'monday': 0,
            'tuesday': 0,
            'wednesday': 0,
            'thursday': 0,
            'friday': 0,
            'saturday': 0,
            'sunday': 0,
        }

        custos_diarios_before = {
            'monday': 0,
            'tuesday': 0,
            'wednesday': 0,
            'thursday': 0,
            'friday': 0,
            'saturday': 0,
            'sunday': 0,
        }

        # Custos da semana atual

        for carregamento in carregamentos.filter(ca_data_inicio__gte=start_of_week):
            dia_da_semana = carregamento.ca_data_inicio.strftime('%A').lower()
            custos_diarios_now[dia_da_semana] += carregamento.ca_custo

        # Custos da semana anterior
        start_of_week_before = start_of_week - timedelta(days=7)
        for carregamento in carregamentos.filter(ca_data_inicio__gte=start_of_week_before, ca_data_inicio__lt=start_of_week):
            dia_da_semana = carregamento.ca_data_inicio.strftime('%A').lower()
            custos_diarios_before[dia_da_semana] += carregamento.ca_custo

        return custos_diarios_now, custos_diarios_before

    def calcular_custos_totais_mensais(self):
        from carregamentos.models import Carregamento

        carregamentos = self.getCarregamentos()
        custos_mensais_now = {i: 0 for i in range(1, 13)}
        custos_mensais_before = {i: 0 for i in range(1, 13)}

        for carregamento in carregamentos:
            mes = carregamento.ca_data_inicio.month
            custos_mensais_now[mes] += carregamento.ca_custo

        for carregamento in carregamentos.filter(ca_data_inicio__year=timezone.now().year - 1):
            mes = carregamento.ca_data_inicio.month
            custos_mensais_before[mes] += carregamento.ca_custo

        return custos_mensais_now, custos_mensais_before


    def __str__(self):
        return self.first_name + " " + self.last_name
