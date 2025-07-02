from django.shortcuts import render
import json
from utilizadores.models import Entidade, Utilizador
from rest_framework.decorators import api_view , permission_classes
from utilizadores.serializer import UtilizadorSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.contrib.auth import authenticate


@permission_classes([AllowAny])
class LoginUtilizadorView(APIView):
    def post(self, request):
        data = request.data

        email = data.get("username")
        password = data.get("password")

        username = email.split('@')[0]  # remover dominio do email
        
        try:
            utilizador = Utilizador.objects.get(username = username)

            serializer = UtilizadorSerializer(utilizador)
            
            utilizador_auth = authenticate(username = utilizador.username, password = password)
            if utilizador_auth is not None:
                utilizador.last_login = timezone.now()
                utilizador.save()
                refresh = RefreshToken.for_user(utilizador_auth)
                return Response({
                    "message": "Login realizado com sucesso!",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": serializer.data
                }, status=200)
            else:
                return Response({"error": "Credenciais invalidas!"}, status= 401)

        except Utilizador.DoesNotExist:
            return Response({"error": "Utilizador não encontrado!"}, status= 404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def LogoutView(request):
    utilizador = request.user.is_authenticated
    data = request.data
    if utilizador:
        refresh_token = data.get("refresh_token")  
        if refresh_token:
            try:
                refresh_token_obj = RefreshToken(refresh_token)
                refresh_token_obj.blacklist()  

                return Response({"message": "Logout realizado com sucesso!"})
            except Exception as e:
                return Response({"error": f"Token inválido ou já expirado! ({str(e)})"})
        else:
            return Response({"error": "Token não fornecido!"})
    else:
        return Response({"error": "Utilizador não autenticado!"})