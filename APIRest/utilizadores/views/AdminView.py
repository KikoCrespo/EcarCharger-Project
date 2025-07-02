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
from rest_framework.permissions import BasePermission


# Tem que ser Authentication
class AdminView(APIView):
    """
    Registar utilizador do tipo admin
    """
    @permission_classes([IsAuthenticated])
    def post(self, request):  
        
        try:
            data = json.loads(request.body)
            user = request.user
            firstName = data.get("first_name")
            lastName = data.get("last_name")
            email = data.get("email")
            password = data.get("password")
            departamento = data.get("u_departamento")
            tipo = data.get("u_tipo")
            print(tipo)
            

            if not email or not password or not departamento:
                return Response({"error": "Todos os campos são obrigatórios!"}, status=400)

            if Utilizador.objects.filter(email = email).exists():
                return Response({"error": "Este Email já está em uso!"}, status=400)
            
            username = email.split('@')[0] # remover domninio do email
            if Utilizador.objects.filter(username = username).exists():
                return Response({"error": "Este Username já está em uso!"}, status=400)
            
            
            dataRegisto = timezone.now()

            utilizador = Utilizador.objects.create(
                first_name= firstName,
                last_name= lastName,
                username=username,
                email=email,
                password = make_password(password),
                date_joined=dataRegisto,
                u_entidade= user.u_entidade,
                is_staff= tipo,
                u_tipo = tipo,
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
        serializer = UtilizadorSerializer(utilizadores, many=True, context={'request': request}) # enviar context para que o serializer reconheça o request e consiga criar um url
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
        

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class PromoverUtilizadorView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, user_id):
        try:
            try:
                user = Utilizador.objects.get(id=user_id)
            except Utilizador.DoesNotExist:
                return Response({"error": "Utilizador não encontrado."}, status=404)

            user.is_staff = True
            user.save()

            return Response({"message": f"Utilizador {user.username} promovido com sucesso."})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class despromoverUtilizadorView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, user_id):
        try:
            try:
                user = Utilizador.objects.get(id=user_id)
            except Utilizador.DoesNotExist:
                return Response({"error": "Utilizador não encontrado."}, status=404)

            user.is_staff = False
            user.save()

            return Response({"message": f"Utilizador {user.username} despromovido com sucesso."})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    

class AlterarUserEstadoView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser] 
    def patch(self, request, user_id):
        try:
            user = Utilizador.objects.get(id=user_id)
        except Utilizador.DoesNotExist:
            return Response({"error": "Utilizador não encontrado."}, status=404)

        novo_estado = request.data.get("novo_estado")  

        if novo_estado is None:
            return Response({"error": "Campo 'novo_estado' é obrigatório."}, status=400)

        user.is_active = novo_estado
        user.u_estado = novo_estado
        user.save()

        return Response({"message": f"Utilizador {user.username} {'ativado' if novo_estado else 'inativado'} com sucesso."})
