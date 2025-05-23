from django.shortcuts import render
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from.serializer import CarregamentoSerializer
from .models import Carregamento
from rest_framework.response import Response
from datetime import datetime
from rest_framework.views import APIView
from utilizadores.models import Utilizador
from automoveis.models import Veiculo
from postosCarregamento.models import PostoCarregamento
from rest_framework import status




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
            id_Veiculo = data.get('ca_Veiculo')
            id_posto = data.get('ca_posto')

            if not all([data_inicio, data_fim, duracao, avg_v, avg_a, avg_kwh, custo, utilizador, Veiculo, posto]):
                return Response({'error': 'Existem campos em falta'}, status=400)
            # Verifica se o utilizador existe
            try:
                utilizador = Utilizador.objects.get(id=id_utilizador)
                if not utilizador.u_estado == 'ativo':
                    return Response({'error': 'Utilizador está desativado'}, status=403)
                
            except Utilizador.DoesNotExist:
                return Response({'error': 'Utilizador não encontrado'}, status=404)
            
            # Verifica se o Veiculo existe
            try:
                Veiculo = Veiculo.objects.get(id= id_Veiculo)
                if not Veiculo.c_estado == 'ativo':
                    return Response({'error': 'Veiculo está desativado'}, status=403)
                
            except Veiculo.DoesNotExist:
                return Response({'error': 'Veiculo não encontrado'}, status=404)
            
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
                ca_Veiculo = Veiculo,
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
            Veiculo = data.get('ca_Veiculo')
            posto = data.get('ca_posto')

            if not all([data_inicio, data_fim, avg_v, avg_a, avg_kwh, custo, utilizador_id, Veiculo, posto]):
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
            carregamento.ca_Veiculo = Veiculo
            carregamento.ca_posto = posto

            
        except Carregamento.DoesNotExist:
                return Response({'error': 'Carregamento não encontrado'}, status=404)
        except Exception as e:
                return Response({'error': str(e)}, status=500)

    @api_view(['POST'])
    @permission_classes([AllowAny])
    def stop_charging_view(request, session_id):
        try:
            carregamento = Carregamento.objects.get(id=session_id)
            medias = request.data
            carregamento.ca_data_fim = datetime.now()
            carregamento.ca_duracao = carregamento.ca_data_fim - carregamento.ca_data_inicio
            carregamento.ca_avg_v = medias['voltage']
            carregamento.ca_avg_a = medias['current']
            carregamento.ca_avg_kwh = medias['power']
            potencia_consumida = medias['power'] * carregamento.ca_duracao.total_seconds() / 3600
            carregamento.ca_custo = potencia_consumida * carregamento.ca_posto.pc_preco_kwh
            carregamento.ca_estado = 'COMPLETED'
            carregamento.save()

            # Enviar ordem para o Flask parar a leitura
            iot_url = carregamento.ca_posto.pc_iot_equipamento.iot_url
            output_pin = carregamento.ca_posto.pc_iot_equipamento.iot_output
            requests.post(f"{iot_url}/stop", json={"output_pin": output_pin})

            return Response({"status": "carregamento terminado"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
def str_to_datetime(date):
    """
    Converte uma string 'YYYY-MM-DD HH:MM:SS' para um objeto datetime.
    """
    formato = "%Y-%m-%dT%H:%M:%S" 
    date_timstamp = datetime.strptime(date, formato)
    return date_timstamp

#só falta adicionar um pequena logica, para além da paragem automarica e depois a conclusao do utilizador, ele pode terminar o carregamento antes da pargem automatica