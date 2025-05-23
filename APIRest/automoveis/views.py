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


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from automoveis.models import Veiculo
from entidades.models import Entidade
from automoveis.serializer import VeiculoSerializer
from automoveis.models import Anexos
from django.utils import timezone
from datetime import datetime

import json

class AddVeiculoEntidadeView(APIView):
    permission_classes = [IsAuthenticated]

    def get_documentos(self, request):
        documentos = []
        index = 0
        while True:
            prefix = f'documentos[{index}]'
            tipo = request.data.get(f'{prefix}[tipo]')
            titulo = request.data.get(f'{prefix}[titulo]')
            data = request.data.get(f'{prefix}[data]')
            validade = request.data.get(f'{prefix}[dataValidade]')
            ficheiro = request.FILES.get(f'{prefix}[ficheiro]')
            print(tipo)
            if not any([tipo, titulo, data, ficheiro]):
                break  # Sai se não houver mais documentos

            documentos.append({
                'tipo': tipo,
                'titulo': titulo,
                'data': data,
                'validade': validade,
                'ficheiro': ficheiro
            })
            index += 1

        return documentos

    def post(self, request):
        try:
            # Campos principais do veículo
            marca = request.data.get("c_marca")
            modelo = request.data.get("c_modelo")
            cor = request.data.get("c_cor")
            matricula = request.data.get("c_matricula")
            potencia = request.data.get("c_potencia")
            lugares = request.data.get("c_lugares")
            categoria = request.data.get("c_categoria")
            combustivel = request.data.get("c_combustivel")
            transmissao = request.data.get("c_transmissao")
            c_registo_ano = request.data.get("c_registo_ano")
            c_registo_mes = request.data.get("c_registo_mes")
            data_aquisicao = request.data.get("c_data_aquisicao")
            quilometros = request.data.get("c_quilometros")
            emissoes = request.data.get("c_emissoes")
            print(marca, modelo, cor, matricula, potencia, lugares, categoria, combustivel, transmissao, c_registo_ano, c_registo_mes, data_aquisicao, quilometros)


            # Processa data de registo
            ano_matricula = None
            if c_registo_ano and c_registo_mes:
                try:
                    ano_matricula = datetime.strptime(f"{c_registo_ano}-{c_registo_mes}-01", "%Y-%m-%d").date()
                except ValueError:
                    print("Data de registo inválida.")
                    return JsonResponse({"error": "Data de registo inválida."}, status=400)

            # Validação básica
            campos_obrigatorios = [marca, modelo, matricula, potencia, lugares, categoria, combustivel, transmissao, quilometros]
            if not all(campos_obrigatorios):
                print("Campos obrigatórios não preenchidos.")
                return JsonResponse({"error": "Preencha todos os campos obrigatórios."}, status=400)

            if Veiculo.objects.filter(v_matricula=matricula).exists():
                print("Matrícula já registada.")
                return JsonResponse({"error": "Esta matrícula já está registada."}, status=400)

            entidade = request.user.u_entidade
            if not entidade:
                return JsonResponse({"error": "Entidade não encontrada."}, status=404)

            # Criação do veículo
            veiculo = Veiculo.objects.create(
                v_marca=marca,
                v_modelo=modelo,
                v_cor=cor,
                v_matricula=matricula,
                v_potencia=potencia,
                v_assentos=lugares,
                v_data_aquisicao=data_aquisicao,
                v_categoria=categoria,
                v_estado=True,
                v_entidade=entidade,
                v_transmissao=transmissao,
                v_combustivel=combustivel,
                v_quilometros=quilometros,
                v_ano_matricula=ano_matricula,
                v_emissoes= emissoes
            )

            # Processa documentos
            documentos = self.get_documentos(request)
            for doc in documentos:
                if(doc['tipo'] == 'Seguro'):
                    doc['tipo'] = 1
                elif(doc['tipo'] == 'Inspeção'):
                    doc['tipo'] = 2
                elif(doc['tipo'] == 'IUC'):
                    doc['tipo'] = 3
                else:
                    doc['tipo'] = 4
                Anexos.objects.create(
                    an_tipo=doc['tipo'],
                    an_titulo=doc['titulo'],
                    an_data=doc['data'],
                    an_data_validade=doc['validade'],
                    an_anexo=doc['ficheiro'],
                    an_veiculo=veiculo
                )

            serializer = VeiculoSerializer(veiculo)
            return Response({
                "message": f"Veículo com matrícula {veiculo.v_matricula} registado com sucesso!",
                "veiculo": serializer.data
            }, status=201)

        except Exception as e:
            print(f"Erro ao processar o pedido: {str(e)}")
            return JsonResponse({"error": f"Ocorreu um erro ao processar o pedido: {str(e)}"}, status=500)


@permission_classes([IsAuthenticated]) 
class getFrotaEntidade(APIView):
    def get(self, request):
        try:
            entidade_id = request.user.u_entidade.id
        except AttributeError:
            return JsonResponse({"error": "Entidade não encontrada!"}, status=404)
        try:
            entidade = Entidade.objects.get(id=entidade_id)
        except Entidade.DoesNotExist:
            return JsonResponse({"error": "Entidade não encontrada!"}, status=404)
        frota = Veiculo.objects.filter(v_entidade=entidade)
        if not frota.exists():
            return JsonResponse({"error": "Não existem Veiculos associados a esta entidade!"}, status=404)
        serializer = VeiculoSerializer(frota, many=True)
        print (frota)

        return Response({"message": "Lista de veiculos","vehicles": serializer.data}, status=200)

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
    
