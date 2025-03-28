from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Entidade
import json


class GetCSRFTokenView(View):
    def get(self, request):
        return JsonResponse({"csrf_token": get_token(request)})
    
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({"error": "Email e password por preencher"}, status=400)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user) 
            csrf_token = get_token(request) 
            return JsonResponse({"message": "Login bem-sucedido!", "csrf_token": csrf_token})
        else:
            return JsonResponse({"error": "Credenciais inválidas"}, status=401)

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({"message": "Logout realizado com sucesso!"})
    
@method_decorator(csrf_exempt, name='dispatch')
class RegistarView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return JsonResponse({"error": "Todos os campos são obrigatórios!"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Este nome de utilizador já existe!"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Este e-mail já está em uso!"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)  # Autentica automaticamente apos o registo

        csrf_token = get_token(request)  # Obtém o CSRF Token para requisições futuras
        return JsonResponse({"message": "Utilizador registado com sucesso!", "csrf_token": csrf_token}, status=201)


from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Entidade
import json

@method_decorator(csrf_exempt, name='dispatch') 
class RegistarEntidadeView(View):
    def post(self, request):
        # Obtenha os dados enviados no corpo da requisição
        data = json.loads(request.body)
        
        # Extraia os dados necessários
        e_nome = data.get("e_nome")
        e_email = data.get("e_email")
        e_nif = data.get("e_nif")
        e_contacto = data.get("e_contacto")
        e_morada = data.get("e_morada")
        e_ordem = data.get("e_ordem")
        e_data_registo = data.get("e_data_registo")
        
        if not e_nome or not e_email or not e_nif:
            return JsonResponse({"error": "Nome, e-mail e NIF são obrigatórios!"}, status=400)
        
        entidade = Entidade.objects.create(
            e_nome=e_nome,
            e_email=e_email,
            e_nif=e_nif,
            e_contacto=e_contacto,
            e_morada=e_morada,
            e_ordem=e_ordem,
            e_data_registo=e_data_registo
        )

        return JsonResponse({"message": "Entidade registrada com sucesso!" + entidade}, status=201)


class LoginEntidadeView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get("email")
        senha = data.get("senha")

        if not email or not senha:
            return JsonResponse({"error": "Email e senha são obrigatórios!"}, status=400)

        try:
            entidade = Entidade.objects.get(e_email=email)
        except Entidade.DoesNotExist:
            return JsonResponse({"error": "Email não encontrado!"}, status=404)

        if entidade.e_senha != senha:
            return JsonResponse({"error": "Senha incorreta!"}, status=401)

        # Se a senha estiver correta, realizar o login (não usar o modelo User)
        # Como a autenticação é feita apenas pela Entidade, vamos usar login customizado
        login(request, entidade)

        csrf_token = get_token(request)
        return JsonResponse({"message": "Login bem-sucedido!", "csrf_token": csrf_token})