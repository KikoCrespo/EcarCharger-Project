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

class PerfilUtilizadorView(APIView):

    permission_classes = [IsAuthenticated]  # Garante que só utilizadores autenticados possam aceder
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            if user.u_img_perfil:  # Verifica se o utilizador tem uma foto
                foto_url = request.build_absolute_uri(user.u_img_perfil.url) #constroi o Url para caminho absoluto

            entidade = user.u_entidade
            return Response({
                'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
                'last_record': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else None,
                'department': user.u_departamento,
                'type': user.is_staff,
                'supa': user.is_superuser,
                'foto_url': foto_url if user.u_img_perfil else None,
                'entidade': entidade.e_nome
            }
        })    
        else:
            return Response({
                'error': 'utilizador não autenticado'
            }, status=401)
        

class FuncionarioView(APIView):

    permission_classes = [IsAuthenticated]  # Garante que só utilizadores autenticados podem aceder
    def post(self, request):
        data = json.loads(request.body)
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "Utilizador não está autenticado!"}, status=401)
        
        if not user.is_staff:
            return Response({"error": "Utilizador não tem permissão para criar outros utilizadores!"}, status=403)
    
        firstName = data.get("first_name")
        lastName = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        departamento = data.get("u_departamento")
        tipo = data.get("u_tipo")
        
        username = email.split('@')[0] # remover domninio do email

        if Utilizador.objects.filter(email = email).exists():
            return Response({"error": "Este email já está em uso!"}, status=400)

        if Utilizador.objects.filter(username = username).exists():
            return Response({"error": "Este Username já está em uso!"}, status=400)
        
        dataRegisto = timezone.now()

        utilizador = Utilizador.objects.create(
            first_name = firstName,
            last_name = lastName,
            username = username,
            email = email,
            password = make_password(password),
            date_joined = dataRegisto,
            u_entidade = user.u_entidade,
            u_departamento= departamento,
            is_staff = tipo,
            u_tipo = tipo,
            u_estado=True
        )
        utilizador.save()
        serializer = UtilizadorSerializer(utilizador)
        
        return Response({
            'message': f"Utilizador {utilizador.first_name} {utilizador.last_name} registado com sucesso!",
            'user': serializer.data
        }, status=201)
    
    def put(self, request):
        try:
            utilizador = request.user  
            if not utilizador.is_authenticated: 
                return Response({"error": "Utilizador não autenticado!"}, status=401)

            data = request.data
            if not data:
                return Response({"error": "Dados não fornecidos!"}, status=400) 

            firstName = data.get("first_name")
            lastName = data.get("last_name")
            password = make_password(data.get("password"))
            departamento = data.get("u_departamento")


            utilizador.first_name = firstName 
            utilizador.last_name = lastName    
            utilizador.password = password
            utilizador.u_departamento = departamento

            if 'foto' in request.FILES:
                utilizador.u_img_perfil = request.FILES['foto']

            utilizador.save() 

            serializer = UtilizadorSerializer(utilizador)

            return Response({
                'message': f"Utilizador {utilizador.first_name} {utilizador.last_name} atualizado com sucesso!",
                'user': serializer.data}, status=200)
        
        except json.JSONDecodeError:
            return Response({"error": "Formato de dados inválido!"}, status=400)
        
        except Utilizador.DoesNotExist:
            return Response({"error": "Utilizador não encontrado!"}, status=404)
        


