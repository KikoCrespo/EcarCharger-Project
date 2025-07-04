# Usa imagem base leve com Python 3.11
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Configura fontes de pacotes confiáveis e atualiza cache
RUN echo "deb http://deb.debian.org/debian bullseye main" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian bullseye-updates main" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org/debian-security bullseye-security main" >> /etc/apt/sources.list

# Instala dependências do sistema
RUN apt-get update -o Acquire::Check-Valid-Until=false -o Acquire::AllowInsecureRepositories=true && \
    apt-get install -y --no-install-recommends \
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
