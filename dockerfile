# Usando a imagem oficial do Python
FROM python:3.11.9

# Instalando dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean

# Setando o diretório de trabalho
WORKDIR /app

# Instalando as dependências do projeto
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o código do projeto
COPY . /app/

# Comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
