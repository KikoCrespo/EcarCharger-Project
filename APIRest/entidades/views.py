from django.shortcuts import render
import json
from .models import Entidade
from rest_framework.decorators import api_view , permission_classes
from .serializer import EntidadeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView



@permission_classes([AllowAny])
class RegistarEntidadeView(APIView):
    def post(self, request):
        """
        regitar uma entidade
        """
        data = json.loads(request.body)
        
        e_nome = data.get("e_nome")
        e_email = data.get("e_email")
        e_nif = data.get("e_nif")
        e_contacto = data.get("e_contacto")
        e_morada = data.get("e_morada")
        e_ordem = data.get("e_ordem")
        e_data_registo = data.get("e_data_registo")
        
        if not e_nome or not e_email or not e_nif:
            return Response({"error": "Nome, Email e NIF são obrigatórios!"}, status=400)
        if Entidade.objects.filter(e_email=e_email).exists() and Entidade.objects.filter(e_nif=e_nif).exists():
            return Response({"error": "Esta Entidade já está inserida no sistema!"}, status=400)
        
        
        entidade = Entidade.objects.create(
            e_nome=e_nome,
            e_email=e_email,
            e_nif=e_nif,
            e_contacto=e_contacto,
            e_morada=e_morada,
            e_ordem=e_ordem,
            e_data_registo=e_data_registo
        )
        entidade.save()
        serializer = EntidadeSerializer(entidade)
        print (entidade)
        return Response({
                        "message": "Entidade registada com sucesso!", 
                        'entidade': serializer.data
                        }, status=201)

