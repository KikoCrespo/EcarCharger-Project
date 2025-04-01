from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Carro
from entidades.models import Entidade
from rest_framework.decorators import permission_classes
from .serializer import CarroSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password


permission_classes([AllowAny]) # tem de ser Authentication
class AddCarroEntidadeView(APIView):
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
            
            if Carro.objects.filter(c_matricula=matricula).exists():
                return JsonResponse({"error": "Esta matricula já está registada!"}, status=400)

            carro = Carro.objects.create(
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

            carro.save()
            serializer = CarroSerializer(carro)
            print (carro)
            return Response({
                            "message": f"Carro com a matricula {carro.c_matricula} registado com sucesso!", 
                            'carro': serializer.data
                            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato de dados inválido!"}, status=400)

@permission_classes([AllowAny]) # tem de ser Authentication
class getFrotaEntidade(APIView):
    def get(self, request, entidade_id):
        try:
            entidade = Entidade.objects.get(id=entidade_id)
        except Entidade.DoesNotExist:
            return JsonResponse({"error": "Entidade não encontrada!"}, status=404)
        frota = Carro.objects.filter(c_entidade=entidade)
        if not frota.exists():
            return JsonResponse({"error": "Não existem carros associados a esta entidade!"}, status=404)
        serializer = CarroSerializer(frota, many=True)
        print (frota)

        return Response(serializer.data, status=200)
