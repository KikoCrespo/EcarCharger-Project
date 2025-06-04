from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PostoCarregamento
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializer import PostoCarregamentotSerializer
from entidades.models import Entidade

# Create your views here.
@permission_classes([IsAuthenticated])
class PostoCarregamentoView(APIView):
    def get(self, request):
        """
        Lista de postos de carregamento
        """

        postos = PostoCarregamento.objects.all()
        if postos.count() == 0:
            return Response({'message': 'Não existem postos de carregamento'}, status= 404)
        serializer = PostoCarregamentotSerializer(postos, many=True)
        return Response({'postos': serializer.data }, status= 200)
    def post(self, request):
        """
        Cria um novo posto de carregamento
        """
        morada = request.data.get('pc_morada')
        data_registo = request.data.get('pc_data_registo')
        intensidade_a = request.data.get('pc_intensidade_a')
        potencia_kw = request.data.get('pc_potencia_kw')
        tipo_ligacao = request.data.get('pc_tipo_ligacao')
        preco_kwh = request.data.get('pc_preco_kwh')
        entidade_id = request.data.get('pc_entidade')
        
        try:
            entidade = Entidade.objects.get(id = entidade_id)
        except Entidade.DoesNotExist:
            return Response({'error': 'Entidade não encontrada'}, status= 404)
        try:
            posto = PostoCarregamento.objects.create(
                pc_morada=morada,
                pc_data_registo=data_registo,
                pc_intensidade_a=intensidade_a,
                pc_potencia_kw=potencia_kw,
                pc_tipo_ligacao=tipo_ligacao,
                pc_preco_kwh=preco_kwh,
                pc_estado= True,
                pc_img= None,
                pc_entidade=entidade
            )

            serializer = PostoCarregamentotSerializer(posto)
            return Response({'Posto': serializer.data}, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status= 400)
    #alterar
    def getPosto(self, request):
        """
        Informação de um posto de carregamento
        """
        posto = PostoCarregamento.objects.get(id=request.data.get('posto_id'))
        if not posto:
            return Response({'message': 'Não existe posto de carregamento'}, status= 404)
        serializer = PostoCarregamentotSerializer(posto)
        return Response({'posto': serializer.data }, status= 200)

class IoTEquipamentoView(APIView):
    def get(self, request):
        """
        Lista de postos de carregamento
        """

        postos = PostoCarregamento.objects.all()
        if postos.count() == 0:
            return Response({'message': 'Não existem postos de carregamento'}, status= 404)
        serializer = PostoCarregamentotSerializer(postos, many=True)
        return Response({'postos': serializer.data }, status= 200)
    def post(self, request):
        """
        Cria um novo posto de carregamento
        """

        nome = request.data.get('iot_nome')
        data_registo = request.data.get('iot_data_registo')
        estado = request.data.get('iot_estado')
        img = request.data.get('iot_img')
        url = request.data.get('iot_url')
        output = request.data.get('iot_output')
        try:
            posto = PostoCarregamento.objects.create(
                iot_nome=nome,
                iot_data_registo=data_registo,
                iot_estado=estado,
                iot_img=img,
                iot_url=url,
                iot_output=output
            )

            serializer = PostoCarregamentotSerializer(posto)
            return Response({'Posto': serializer.data}, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status= 400)

