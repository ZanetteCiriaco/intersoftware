# Use a imagem base python:3.11-alpine
FROM python:3.11-alpine

# Defina as variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

# Instale as dependências necessárias para compilar dependências Python
RUN apk update && apk add --no-cache \
    # Required for installing/upgrading psycopg2 (PostgreSQL client) and Pillow (image library):
    gcc python3-dev musl-dev \
    # Required for installing/upgrading psycopg2:
    postgresql-libs postgresql-dev

# Crie o diretório de trabalho
RUN mkdir /code
WORKDIR /code

# Instale o utilitário pipenv
RUN pip install --upgrade pipenv

# Copie os arquivos Pipfile e Pipfile.lock para o diretório de trabalho do contêiner
COPY Pipfile Pipfile.lock /code/

# Instale as dependências usando o Pipenv
RUN pipenv install --deploy --system

# Copie o código do projeto para o diretório de trabalho do contêiner
COPY . /code/