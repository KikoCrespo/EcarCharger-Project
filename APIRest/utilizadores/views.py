from django.shortcuts import render
import json
from .models import Entidade, Utilizador
from rest_framework.decorators import api_view , permission_classes
from .serializer import UtilizadorSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.contrib.auth import authenticate



@permission_classes([IsAuthenticated])     # Tem que ser Authentication
class AdminView(APIView):
    """
    Registar utilizador do tipo admin
    """
    def post(self, request):  
        
        try:
            data = request.body
            firstName = data.get("primeiro_nome")
            lastName = data.get("ultimo_nome")
            email = data.get("u_email")
            password = data.get("u_password")
            entidade_id = data.get("u_entidade")
            tipo = data.get("u_tipo")
            

            if not email or not password or not entidade_id:
                return Response({"error": "Todos os campos são obrigatórios!"}, status=400)

            if Utilizador.objects.filter(email = email).exists():
                return Response({"error": "Este Email já está em uso!"}, status=400)
            
            username = email.split('@')[0] # remover domninio do email
            if Utilizador.objects.filter(username = username).exists():
                return Response({"error": "Este Username já está em uso!"}, status=400)
            
            try:
                entidade = Entidade.objects.get(id=entidade_id)
            except Entidade.DoesNotExist:
                return Response({"error": "Entidade não encontrada!"}, status=404)
            
            dataRegisto = timezone.now()

            utilizador = Utilizador.objects.create(
                first_name= firstName,
                last_name= lastName,
                username=username,
                email=email,
                password = make_password(password),
                date_joined=dataRegisto,
                u_entidade=entidade,
                u_tipo=tipo,
                u_estado=True,
                u_img_perfil= None,
            )
            

            token = RefreshToken.for_user(utilizador)
            print (token)
            serializer = UtilizadorSerializer(utilizador)
            utilizador.save()
            print (utilizador.id)

            return Response({
                'message': f"Utilizador {utilizador.first_name} {utilizador.last_name} registado com sucesso!",
                'access': str(token.access_token),
                'refresh': str(token),
                'user': serializer.data
            }, status=201)

        except json.JSONDecodeError:
            return Response({"error": "Formato de dados inválido!"}, status=400)
    
    """
    Listar utilizadores
    """
    @permission_classes([IsAuthenticated])
    def get(self, request):
        utilizadores = Utilizador.objects.all()
        serializer = UtilizadorSerializer(utilizadores, many=True)
        return Response({"message": "Lista de utilizadores","users": serializer.data }, status=200)
    """
    Atualizar utilizador
    """
    @permission_classes([IsAuthenticated])
    def put(self, request):
        try:
            utilizador = request.user  
            if not utilizador.is_authenticated: 
                return Response({"error": "Utilizador não autenticado!"}, status=401)

            data = json.loads(request.body) 

            firstName = data.get("primeiro_nome")
            lastName = data.get("ultimo_nome")
            password = make_password(data.get("u_password"))
            entidade_id = data.get("u_entidade")
            dataRegisto = data.get("u_data_registo")
            tipo = data.get("u_tipo")
            imagem = data.get("u_img_perfil")
            estado = data.get("u_estado")
            print(entidade_id)

            try:
                entidade = Entidade.objects.get(id=entidade_id)
            except Entidade.DoesNotExist:
                return Response({"error": "Entidade não encontrada!"}, status=404)

            utilizador.first_name = firstName 
            utilizador.last_name = lastName    
            utilizador.password = password
            utilizador.u_data_registo = dataRegisto
            utilizador.u_entidade = entidade
            utilizador.u_tipo = tipo
            utilizador.u_estado = estado
            utilizador.u_img_perfil = imagem
            utilizador.save() 

            serializer = UtilizadorSerializer(utilizador)

            return Response({
                'message': f"Utilizador {utilizador.first_name} {utilizador.last_name} atualizado com sucesso!",
                'user': serializer.data}, status=200)
        
        except json.JSONDecodeError:
            return Response({"error": "Formato de dados inválido!"}, status=400)
        
        except Utilizador.DoesNotExist:
            return Response({"error": "Utilizador não encontrado!"}, status=404)

        

"""  
Login do Utilizador
"""
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
    

class PerfilUtilizadorView(APIView):
    permission_classes = [IsAuthenticated]  # Garante que só utilizadores autenticados podem aceder

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            return Response({
                'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
                'last_record': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else None,
                'type': user.is_staff,
                'supa': user.is_superuser
            }
        })    
        else:
            return Response({
                'error': 'utilizador não autenticado'
            }, status=401)

class FuncionarioView(APIView):
    permission_classes = [IsAuthenticated]  # Garante que só utilizadores autenticados podem aceder

    def post(self, request):
        data = request.data
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "Utilizador não está autenticado!"}, status=401)
        
        if not user.is_staff:
            return Response({"error": "Utilizador não tem permissão para criar outros utilizadores!"}, status=403)
    
        firstName = data.get("primeiro_nome")
        lastName = data.get("ultimo_nome")
        email = data.get("u_email")
        password = data.get("u_password")
        entidade_id = data.get("u_entidade")
        tipo = data.get("u_tipo")
        
        username = email.split('@')[0] # remover domninio do email

        if Utilizador.objects.filter(email = email).exists():
            return Response({"error": "Este email já está em uso!"}, status=400)

        if Utilizador.objects.filter(username = username).exists():
            return Response({"error": "Este Username já está em uso!"}, status=400)
        try:
            entidade = Entidade.objects.get(id=entidade_id)
        except Entidade.DoesNotExist:
            return Response({"error": "Entidade não encontrada!"}, status=404)
        
        dataRegisto = timezone.now()

        utilizador = Utilizador.objects.create(
            first_name= firstName,
            last_name= lastName,
            username=username,
            email=email,
            password = make_password(password),
            date_joined=dataRegisto,
            u_entidade=entidade,
            u_tipo=tipo,
            u_estado=True
        )
        utilizador.save()
        serializer = UtilizadorSerializer(utilizador)
        
        return Response({
            'message': f"Utilizador {utilizador.first_name} {utilizador.last_name} registado com sucesso!",
            'user': serializer.data
        }, status=201)
    