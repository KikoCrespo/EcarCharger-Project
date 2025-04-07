from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from.serializer import CarregamentoSerializer
from .models import Carregamento
from rest_framework.response import Response
from datetime import datetime
from rest_framework.views import APIView
from utilizadores.models import Utilizador
from automoveis.models import Carro
from postosCarregamento.models import PostoCarregamento


@permission_classes([AllowAny])
class CarregamentosView(APIView):
    def get(self, request):
        """
        Lista de carregamentos
        """
        carregamentos = Carregamento.objects.all()
        serializer = CarregamentoSerializer(carregamentos, many=True)
        return Response({'carregamentos',serializer.data}, status=200)
    
    def post(self, request):
        """
        Inicia um carregamento
        """
        try:
            data = request.data.get('data')
            data_inicio = data.get('ca_data_inicio')
            data_fim = data.get('ca_data_fim')
            duracao = data.get('ca_duracao')
            avg_v = data.get('ca_avg_v')
            avg_a = data.get('ca_avg_a')
            avg_kwh = data.get('ca_avg_kwh')
            custo = data.get('ca_custo')
            id_utilizador = data.get('ca_utilizador')
            id_carro = data.get('ca_carro')
            id_posto = data.get('ca_posto')

            if not all([data_inicio, data_fim, duracao, avg_v, avg_a, avg_kwh, custo, utilizador, carro, posto]):
                return Response({'error': 'Existem campos em falta'}, status=400)
            # Verifica se o utilizador existe
            try:
                utilizador = Utilizador.objects.get(id=id_utilizador)
                if not utilizador.u_estado == 'ativo':
                    return Response({'error': 'Utilizador está desativado'}, status=403)
                
            except Utilizador.DoesNotExist:
                return Response({'error': 'Utilizador não encontrado'}, status=404)
            
            # Verifica se o carro existe
            try:
                carro = Carro.objects.get(id= id_carro)
                if not carro.c_estado == 'ativo':
                    return Response({'error': 'Carro está desativado'}, status=403)
                
            except Carro.DoesNotExist:
                return Response({'error': 'Carro não encontrado'}, status=404)
            
            # Verifica se o posto existe
            try:
                posto = PostoCarregamento.objects.get(id= id_posto)
                if not posto.p_estado == 'ativo':
                    return Response({'error': 'Posto está desativado'}, status=403)
                
            except PostoCarregamento.DoesNotExist:
                return Response({'error': 'Posto não encontrado'}, status=404)
            
            # Verifica se o carregamento já existe
            carregamento =Carregamento.objects.create(
                ca_data_inicio= data_inicio,
                ca_data_fim= data_fim,
                ca_duracao= duracao,
                ca_avg_v = avg_v,
                ca_avg_a = avg_a,
                ca_avg_kwh = avg_kwh,
                ca_custo = custo,
                ca_utilizador = utilizador,
                ca_carro = carro,
                ca_posto = posto
            )
            
            serializer = CarregamentoSerializer(carregamento)
            if serializer.is_valid():
                serializer.save()
                return Response({'carregamento': serializer.data}, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    def put(self, request, id):
        """
        Atualiza um carregamento
        """
        try:
            carregamento = Carregamento.objects.get(id=id)
            data = request.data.get('ca_data')
            data_inicio_str = data.get('ca_data_inicio')
            data_fim_str= data.get('ca_data_fim')
            data_inicio = str_to_datetime(data_inicio_str)
            data_fim= str_to_datetime(data_fim_str)
            avg_v = data.get('ca_avg_v')
            avg_a = data.get('ca_avg_a')
            avg_kwh = data.get('ca_avg_kwh')
            custo = data.get('ca_custo')
            utilizador_id = data.get('ca_utilizador')
            carro = data.get('ca_carro')
            posto = data.get('ca_posto')

            if not all([data_inicio, data_fim, avg_v, avg_a, avg_kwh, custo, utilizador_id, carro, posto]):
                return Response({'error': 'Existem campos em falta'}, status=400)

            duracao = data_fim - data_inicio   

            utilizador = Utilizador.objects.get(id=utilizador_id)
            if not utilizador.u_estado == 'ativo':
                return Response({'error': 'Utilizador está desativado'}, status=403)
        

            # atualizar o carregamento
            carregamento.ca_data_inicio= data_inicio
            carregamento.ca_data_fim= data_fim
            carregamento.ca_duracao= duracao
            carregamento.ca_avg_v = avg_v
            carregamento.ca_avg_a = avg_a
            carregamento.ca_avg_kwh = avg_kwh
            carregamento.ca_custo = custo
            carregamento.ca_utilizador = utilizador
            carregamento.ca_carro = carro
            carregamento.ca_posto = posto

            
        except Carregamento.DoesNotExist:
                return Response({'error': 'Carregamento não encontrado'}, status=404)
        except Exception as e:
                return Response({'error': str(e)}, status=500)
            
    
def str_to_datetime(date):
    """
    Converte uma string 'YYYY-MM-DD HH:MM:SS' para um objeto datetime.
    """
    formato = "%Y-%m-%dT%H:%M:%S" 
    date_timstamp = datetime.strptime(date, formato)
    return date_timstamp
