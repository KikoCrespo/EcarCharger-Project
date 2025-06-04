from django.shortcuts import render
from django.http import JsonResponse
import json
from automoveis.models import Veiculo
from entidades.models import Entidade
from rest_framework.decorators import permission_classes
from automoveis.serializer import VeiculoSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from automoveis.models import Veiculo , Anexos, Requisicao
from entidades.models import Entidade
from automoveis.serializer import VeiculoSerializer, AnexosSerializer, RequisicaoSerializer
from django.utils import timezone
from datetime import datetime, timedelta


@permission_classes([IsAuthenticated])
class requisicaoView(APIView):
    def get(self, request):
        try:
            user = request.user
            if not user.is_authenticated:
                return Response({"error": "Utilizador não autenticado."}, status=401)

            entidade = user.u_entidade
            if not entidade:
                return Response({"error": "Entidade não encontrada."}, status=404)

            if user.is_staff:
                requisicoes = Requisicao.objects.filter(r_entidade=entidade).order_by('-r_data_inicio')
            else:
                return Response({"error": "Acesso negado. Apenas utilizadores com permissões de administrativas podem ver todas as requisições."}, status=403)

            if not requisicoes.exists():
                return Response({"message": "Nenhuma requisição encontrada."}, status=404)

            serializer = RequisicaoSerializer(requisicoes, many=True)
            print(f"Requisições encontradas: {serializer.data}")
            return Response({"requisicoes": serializer.data}, status=200)

        except Exception as e:
            print(f"Erro ao processar a requisição: {str(e)}")
            return Response({"error": f"Ocorreu um erro ao processar a requisição: {str(e)}"}, status=500)


    def post(self, request):
        try:
            data = request.data
            veiculo_id = data.get("veiculo_id")
            r_utilizador = request.user
            r_motivo = data.get("motivo")
            r_data_inicio = data.get("data_inicio")
            r_data_fim = data.get("data_fim")
            r_ilimitado = data.get("ilimitado", False)
            entidade = request.user.u_entidade

            if not entidade:
                return Response({"error": "Entidade não encontrada."}, status=404)


            if not r_data_inicio:
                return Response({"error": "Data de início não fornecida."}, status=400)
            
            if (r_ilimitado and r_data_fim) or (not r_ilimitado and not r_data_fim):
                return Response({"error": "A requisição deve ter apenas uma data final"},status=400)

            if not r_utilizador:
                return Response({"error": "Utilizador não autenticado."}, status=401)
            
            if not veiculo_id:
                return Response({"error": "ID do veículo não fornecido."}, status=400)
            
            try:
                veiculo = Veiculo.objects.get(id=veiculo_id)
            except Veiculo.DoesNotExist:
                return Response({"error": "Veículo não encontrado."}, status=404)
            
            Requisicao.objects.create(  
                r_utilizador=r_utilizador,
                r_veiculo=veiculo,
                r_motivo=r_motivo,
                r_data_inicio=r_data_inicio,
                r_data_fim=r_data_fim,
                r_ilimitado=r_ilimitado,
                r_estado=1, # Pendente
                r_entidade=entidade
            )
            return Response({"message": "Requisição de veículo criada com sucesso!"}, status=201)
        except Exception as e:
            print(f"Erro ao processar a requisição: {str(e)}")
            return Response({"error": f"Ocorreu um erro ao processar a requisição: {str(e)}"}, status=500)
        


class RequisicoesVeiculoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, veiculo_id):
        try:
            today = datetime.now()
            first_day_of_current_month = today.replace(day=1)
            first_day_of_last_month = (first_day_of_current_month - timedelta(days=1)).replace(day=1)
            
            veiculo = Veiculo.objects.get(id=veiculo_id)
            requisicoes = Requisicao.objects.filter(r_veiculo=veiculo)
            serializer = RequisicaoSerializer(requisicoes, many=True)
            return Response({'requisicoes': serializer.data}, status=200)
        except Veiculo.DoesNotExist:
            return Response({'error': 'Veículo não encontrado'}, status=404)
        except Exception as e:
            print(f"Erro ao processar a requisição: {str(e)}")
            return Response({'error': str(e)}, status=500)
        




class RequisicaoUtilizadorView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            if not user.is_authenticated:
                return Response({"error": "Utilizador não autenticado."}, status=401)

            requisicoes = Requisicao.objects.filter(r_utilizador=user).order_by('-r_data_inicio')
            if not requisicoes.exists():
                return Response({"message": "Nenhuma requisição encontrada."}, status=404)

            serializer = RequisicaoSerializer(requisicoes, many=True)
            return Response({"requisicoes": serializer.data}, status=200)

        except Exception as e:
            print(f"Erro ao processar a requisição: {str(e)}")
            return Response({"error": f"Ocorreu um erro ao processar a requisição: {str(e)}"}, status=500)
        
    def put(self, request):
        try:   
            requisicao_id = request.data.get('requisicao_id')
            novo_estado = request.data.get('novo_estado')
            motivo_terminacao = request.data.get('motivo_terminacao', None)
            user = request.user
            if not user.is_authenticated:
                return Response({"error": "Utilizador não autenticado."}, status=401)

            try:
                requisicao = Requisicao.objects.get(id=requisicao_id)
            except Requisicao.DoesNotExist:
                print("Requisição não encontrada.")
                return Response({"error": "Requisição não encontrada."}, status=404)

            if novo_estado not in [1, 2, 3,4]:
                print("Estado inválido.")
                return Response({"error": "Estado inválido."}, status=404)

            if requisicao.r_estado == 2 and novo_estado == 2:
                print("Requisição já aprovada.")
                return Response({"error": "Requisição já aprovada."}, status=404)

            if requisicao.r_estado == 3 and novo_estado == 3:
                return Response({"error": "Requisição já rejeitada."}, status=400)
            
            if requisicao.r_estado == 4 and novo_estado == 4:
                return Response({"error": "Requisição já cancelada."}, status=400)


            requisicao.r_estado = novo_estado
            requisicao.save()
            if (requisicao.r_estado == 2):
                veiculo = requisicao.r_veiculo
                veiculo.v_estado = 4
                veiculo.save()
            elif (requisicao.r_estado == 3):
                veiculo = requisicao.r_veiculo
                veiculo.v_estado = 1
                veiculo.save()
            elif (requisicao.r_estado == 4):
                veiculo = requisicao.r_veiculo
                veiculo.v_estado = 1
                veiculo.save()
                requisicao.r_data_fim = timezone.now()
                requisicao.r_motivo_terminacao = motivo_terminacao or f"Requisição cancelada pelo utilizador {user.first_name} {user.last_name}"
                requisicao.save()
            return Response({"message": "Estado atualizado com sucesso."}, status=200)
        
        except Exception as e:
            print(f"Erro ao atualizar o estado da requisição: {str(e)}")
            return Response({"error": f"Ocorreu um erro ao atualizar o estado da requisição: {str(e)}"}, status=500)