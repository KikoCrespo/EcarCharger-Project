from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Veiculo
from entidades.models import Entidade
from rest_framework.decorators import permission_classes
from .serializer import VeiculoSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


permission_classes([AllowAny]) # tem de ser Authentication
class AddVeiculoEntidadeView(APIView):
    def post(self, request): 
        try:
            data = json.loads(request.body)
            marca = data.get("c_marca")
            modelo = data.get("c_modelo")
            ano = data.get("c_ano")
            entidade_id = data.get("e_id")
            matricula = data.get("c_matricula")
            potencia = data.get("c_potencia")
            data_registo = data.get("c_data_registo")
            data_e_mes = data.get("c_ano_e_mes")
            categoria = data.get("c_categoria")

            if not marca or not modelo or not ano or not entidade_id or not matricula or not potencia or not data_registo or not data_e_mes or not categoria:
                return JsonResponse({"error": "Todos os campos são obrigatórios!"}, status=400)
            
            try:
                entidade = Entidade.objects.get(id=entidade_id)
            except Entidade.DoesNotExist:
                return JsonResponse({"error": "Entidade não encontrada!"}, status=404)
            
            if Veiculo.objects.filter(c_matricula=matricula).exists():
                return JsonResponse({"error": "Esta matricula já está registada!"}, status=400)

            Veiculo = Veiculo.objects.create(
                c_marca=marca,
                c_modelo=modelo,
                c_matricula= matricula,
                c_entidade=entidade,
                c_potencia= potencia,
                c_data_registo= data_registo,
                c_ano_e_mes= data_e_mes,
                c_categoria= categoria,
                c_estado=True
            )

            Veiculo.save()
            serializer = VeiculoSerializer(Veiculo)
            print (Veiculo)
            return Response({
                            "message": f"Veiculo com a matricula {Veiculo.c_matricula} registado com sucesso!", 
                            'Veiculo': serializer.data
                            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato de dados inválido!"}, status=400)

@permission_classes([IsAuthenticated]) 
class getFrotaEntidade(APIView):
    def get(self, request, entidade_id):
        try:
            entidade = Entidade.objects.get(id=entidade_id)
        except Entidade.DoesNotExist:
            return JsonResponse({"error": "Entidade não encontrada!"}, status=404)
        frota = Veiculo.objects.filter(c_entidade=entidade)
        if not frota.exists():
            return JsonResponse({"error": "Não existem Veiculos associados a esta entidade!"}, status=404)
        serializer = VeiculoSerializer(frota, many=True)
        print (frota)

        return Response(serializer.data, status=200)

@permission_classes([IsAuthenticated]) 
class  getVeiculosUtilizador(APIView):
    def get(self, request):
        try:
            utilizador = request.user.is_authenticated
        except Exception as e:
            return JsonResponse({"error": "Utilizador não autenticado!" }, status=401)
        
        Veiculos = Veiculo.objects.filter(c_utilizador=utilizador)
        if not Veiculos.exists():
            return JsonResponse({"error": "Não existem Veiculos associados a este utilizador!"}, status=404)
        serializer = VeiculoSerializer(Veiculos, many=True)
        print (Veiculos)
        return Response({"user": utilizador, "Veiculos": serializer.data}, status=200)
    
