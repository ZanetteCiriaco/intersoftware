# Intersoftware CRUD

## 1. Instalar o Docker
Se você ainda não tem o Docker instalado, https://www.docker.com/

## 2. Configurar o arquivo .env
Crie um arquivo chamado .env na raiz do projeto e adicione as seguintes variáveis de ambiente com os valores fornecidos:



````
DEBUG=True
SECRET_KEY=
ALLOWED_HOSTS=*

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=db

````

Substitua os campos em branco pelas informações apropriadas, como a chave SECRET_KEY, credenciais do banco de dados (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB), entre outros.

## 3. Executar o Docker Compose
Com o arquivo .env configurado corretamente, agora você pode executar o Docker Compose para construir e executar a aplicação. Abra um terminal na pasta do projeto (onde está localizado o arquivo docker-compose.yml) e execute os seguintes comando:

````
docker-compose build
````
````
docker-compose up
````

## 4. Acessar a aplicação
Após a conclusão dos passos anteriores e se tudo ocorreu bem, sua aplicação estará em execução. Você poderá acessá-la através do navegador da web em http://localhost:8000/
