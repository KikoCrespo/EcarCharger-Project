from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json


class GetCSRFTokenView(View):
    def get(self, request):
        return JsonResponse({"csrf_token": get_token(request)})
    
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({"error": "Email e password por preencher"}, status=400)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user) 
            csrf_token = get_token(request) 
            return JsonResponse({"message": "Login bem-sucedido!", "csrf_token": csrf_token})
        else:
            return JsonResponse({"error": "Credenciais inválidas"}, status=401)

class LogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({"message": "Logout realizado com sucesso!"})

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
