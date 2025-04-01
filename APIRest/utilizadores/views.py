from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Entidade, Utilizador
from rest_framework.decorators import api_view , permission_classes
from .serializer import UtilizadorSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password



@permission_classes([AllowAny])
class LoginUtilizadorView(APIView):
    def post(self, request):
        data = request.data
        email = data.get("u_email")
        password = data.get("u_password")

        try:
            utilizador = Utilizador.objects.get(u_email=email)

            
            if check_password(password, utilizador.u_password):
                refresh = RefreshToken.for_user(utilizador)

                return Response({
                    "message": "Login realizado com sucesso!",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }, status=200)
            else:
                return Response({"error": "Password incorreta!"}, status=401)

        except Utilizador.DoesNotExist:
            return Response({"error": "Utilizador não encontrado!"}, status=404)

# por fazer
@api_view(['POST'])
def LogoutView(request):
        
        return JsonResponse({"message": "Logout realizado com sucesso!"})

@permission_classes([AllowAny])     # Tem que ser Authentication
class RegistarUtilizadorView(APIView):
    def post(self, request):
        
        try:
            data = json.loads(request.body)
            nome = data.get("u_nome")
            email = data.get("u_email")
            password = data.get("u_password")
            entidade_id = data.get("e_id")
            dataRegisto = data.get("u_data_registo")
            tipo = data.get("u_tipo")
            imagem = data.get("u_img_perfil")

            if not nome or not email or not password or not entidade_id or not dataRegisto:
                return JsonResponse({"error": "Todos os campos são obrigatórios!"}, status=400)

            if Utilizador.objects.filter(u_email=email).exists():
                return JsonResponse({"error": "Este Email já está em uso!"}, status=400)

            try:
                entidade = Entidade.objects.get(id=entidade_id)
            except Entidade.DoesNotExist:
                return JsonResponse({"error": "Entidade não encontrada!"}, status=404)

            utilizador = Utilizador.objects.create(
                u_nome=nome,
                u_email=email,
                u_password=make_password(password), #hash
                u_data_registo=dataRegisto,
                u_entidade=entidade,
                u_tipo=tipo,
                u_estado=True,
                u_token=None,
                u_img_perfil=imagem
            )
            

            token = RefreshToken.for_user(utilizador)
            print (token)
            serializer = UtilizadorSerializer(utilizador)
            utilizador.save()
            print (utilizador.id)

            return Response({
                'message': f"Utilizador {utilizador.u_nome} registado com sucesso!",
                'access': str(token.access_token),
                'refresh': str(token),
                'user': serializer.data
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato de dados inválido!"}, status=400)


