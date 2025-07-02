# Usa imagem base leve com Python 3.11
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instala dependências do sistema (necessárias para psycopg2, cryptography, etc)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    libffi-dev \
    libssl-dev \
    netcat \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia os ficheiros do projeto para o container
COPY . .

# Instala as dependências Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia ficheiros de ambiente se usares `.env`
# COPY .env .env

# Coleta os ficheiros estáticos (produção)
RUN python manage.py collectstatic --noinput

# Expõe a porta padrão usada pelo Daphne (ou Gunicorn)
EXPOSE 8000

# Comando para iniciar o servidor ASGI (Channels + Django)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "APIRest.asgi:application"]
