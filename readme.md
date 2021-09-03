# KMDb

O KMDb é uma plataforma de cadastro e reviews de filmes, semelhante ao IMDb.

# Este passo é para baixar o projeto

`git clone https://gitlab.com/carlosbentz/kmdb`

## Entrar na pasta

`cd kmdb`

## Criar um ambiente virtual

`python3 -m venv venv`

## Entrar no ambiente virtual

`source venv/bin/activate`

## Instalar as dependências

`pip install -r requirements.txt`

## Criar o banco de dados

`./manage.py migrate`

## Rodar localmente

`./manage.py runserver`

Por padrão, irá rodar em `http://127.0.0.1:8000/`

# Testes

## Rodar os testes

Para rodar os testes, apenas utilizar o comando no terminal:

` TEST=TEST python manage.py test -v 2 &> report.txt`

## Sobre Usuários:

Esta plataforma terá 3 tipos de usuário:

- Admin
- Crítico

Para diferenciar entre os tipos de usuários, você deverá trabalhar com os campos `is_staff` e `is_superuser`, sendo que:

- Admin - terá ambos os campos `is_staff` e `is_superuser` com o valor `True`
- Crítico - terá os campos `is_staff` == `True` e `is_superuser` == `False`

# Rotas

## Sobre Criação de Usuários:

### `POST /api/accounts/`

```json
// REQUEST
{
  "username": "critic",
  "password": "1234",
  "first_name": "John",
  "last_name": "Wick",
  "is_superuser": false,
  "is_staff": true
}
```

```json
// RESPONSE STATUS -> HTTP 201
{
  "id": 1,
  "username": "critic",
  "first_name": "John",
  "last_name": "Wick",
  "is_superuser": false,
  "is_staff": true
}
```

Caso haja a tentativa de criação de um usuário que já está cadastrado o sistema irá responder com `HTTP 400 - BAD REQUEST`.

## Sobre Autenticação:

A API funcionará com autenticação baseada em token.

### `POST /api/login/`

```json
// REQUEST
{
  "username": "critic",
  "password": "1234"
}
```

```json
// RESPONSE STATUS -> HTTP 200
{
  "token": "dfd384673e9127213de6116ca33257ce4aa203cf"
}
```

Esse token servirá para identificar o usuário em cada request. Na grande maioria dos endpoints seguintes, será necessário colocar essa informação nos `Headers`. O header específico para autenticação tem o formato `Authorization: Token <colocar o token aqui>`.

Caso haja a tentativa de login de uma conta que ainda não tenha sido criada, o sistema irá retornar HTTP 401 - Unauthorized.

## Sobre Movies:

Esse endpoint só poderá ser acesso por um usuário do tipo admin, e será responsável por criar filmes na plataforma KMDb.

### `POST /api/movies/`

```json
// REQUEST
// Header -> Authorization: Token <token-do-admin>
{
  "title": "O Poderoso Chefão 2",
  "duration": "175m",
  "genres": [{ "name": "Crime" }, { "name": "Drama" }],
  "premiere": "1972-09-10",
  "classification": 14,
  "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' ..."
}
```

```json
// RESPONSE STATUS -> HTTP 201 CREATED
{
  "id": 1,
  "title": "O Poderoso Chefão 2",
  "duration": "175m",
  "genres": [
    {
      "id": 1,
      "name": "Crime"
    },
    {
      "id": 2,
      "name": "Drama"
    }
  ],
  "premiere": "1972-09-10",
  "classification": 14,
  "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ..."
}
```

Não deve ser possível realizar a criação de dois gêneros com o mesmo nome, caso isso aconteça, a aplicação deverá retornar o gênero que está cadastrado no sistema.

### `GET /api/movies/` - Rota que lista todos os filmes cadastrados

Este endpoint pode ser acessado por qualquer client (mesmo sem autenticação). A resposta do servidor será uma lista dos filmes cadastrados.

```json
// RESPONSE STATUS -> 200 OK
[
  {
    "id": 1,
    "title": "O Poderoso Chefão 2",
    "duration": "175m",
    "genres": [
      {
        "id": 1,
        "name": "Crime"
      },
      {
        "id": 2,
        "name": "Drama"
      }
    ],
    "premiere": "1972-09-10",
    "classification": 14,
    "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' ..."
  },
  {
    "id": 2,
    "title": "Um Sonho de Liberdade",
    "duration": "142m",
    "genres": [
      {
        "id": 2,
        "name": "Drama"
      },
      {
        "id": 4,
        "name": "Ficção científica"
      }
    ],
    "premiere": "1994-10-14",
    "classification": 16,
    "synopsis": "Andy Dufresne é condenado a duas prisões perpétuas..."
  }
]
```

### `GET /api/movies/` - Rota que lista todos os filmes cadastrados com base na filtragem do request

Este endpoint pode ser acessado por qualquer client (mesmo sem autenticação).

Esta rota irá fazer uma filtragem dinâmica, para poder buscar qualquer filme pelo título. Nesse caso, todos os filmes que tiverem a palavra "liberdade" no título deverão ser retornados.

```json
// REQUEST
{
  "title": "liberdade" // Campo obrigatório
}
```

```json
// RESPONSE STATUS 200 OK
[
  {
    "id": 2,
    "title": "Um Sonho de Liberdade",
    "duration": "142m",
    "genres": [
      {
        "id": 2,
        "name": "Drama"
      },
      {
        "id": 3,
        "name": "Ficção científica"
      }
    ],
    "premiere": "1994-10-14",
    "classification": 16,
    "synopsis": "Andy Dufresne é condenado a duas prisões perpétuas..."
  },
  {
    "id": 3,
    "title": "Em busca da liberdade",
    "duration": "175m",
    "genres": [
      {
        "id": 2,
        "name": "Drama"
      },
      {
        "id": 4,
        "name": "Obra de época"
      }
    ],
    "premiere": "2018-02-22",
    "classification": 14,
    "synopsis": "Representando a Grã-Bretanha,  corredor Eric Liddell"
  }
]
```

Perceba que só foram filtrados filmes que possuam a palavra "liberdade" no título.

### `GET /api/movies/<int:movie_id>/` - Rota que busca o filme especificado pelo id

Este endpoint pode ser acessado por qualquer client (mesmo sem autenticação). A resposta do servidor é o filme filtrado pelo movie_id.

**Importante!**

Caso o usuário esteja autenticado, um campo com as reviews será mostrado juntamente com o retorno, caso contrário não será mostrado o campo com as reviews.

```json
// REQUEST
// Header -> Authorization: Token <token-do-critic ou token-do-admin>

```

```json
// RESPONSE STATUS -> HTTP 200 OK
{
  "id": 9,
  "title": "Nomadland",
  "duration": "110m",
  "genres": [
    {
      "id": 2,
      "name": "Drama"
    },
    {
      "id": 4,
      "name": "Obra de Época"
    }
  ],
  "premiere": "2021-04-15",
  "classification": 14,
  "synopsis": "Uma mulher na casa dos 60 anos que, depois de perder...",
  "reviews": [
    {
      "id": 5,
      "critic": {
        "id": 1,
        "first_name": "Jacques",
        "last_name": "Aumont"
      },
      "stars": 8,
      "review": "Nomadland apresenta fortes credenciais para ser favorito ...",
      "spoilers": false
    }
  ]
}
```

Observe que o campo reviews foi mostrado no retorno.

Esse deverá ser o retorno caso um usuário anônimo tente acessar esse endpoint.

```json
// RESPONSE STATUS -> HTTP 200 OK
{
  "id": 9,
  "title": "Nomadland",
  "duration": "110m",
  "genres": [
    {
      "id": 2,
      "name": "Drama"
    },
    {
      "id": 4,
      "name": "Obra de Época"
    }
  ],
  "premiere": "2021-04-15",
  "classification": 14,
  "synopsis": "Uma mulher na casa dos 60 anos que, depois de perder..."
}
```

Caso seja passado um movie_id inválido, deverá retornar um erro `HTTP 404 - NOT FOUND`.

```json
// RESPONSE STATUS -> HTTP 404 NOT FOUND
{
  "detail": "Not found."
}
```

### `DELETE /api/movies/<int:movie_id>/` - Rota que deleta filmes

Somente um usuário do tipo admin poderá deletar filmes.

Ao excluir um filme da plataforma, também devem ser removidos todos os reviews.

Se for possível deletar deve ser retornado um status `HTTP 204 - No Content`.

```json
// REQUEST
// Header -> Authorization: Token <token-do-admin>

```

```json
// RESPONSE STATUS -> HTTP 204

```

Caso seja passado um movie_id inválido, deverá retornar um erro `HTTP 404 - NOT FOUND`.

```json
// RESPONSE STATUS -> HTTP 404 NOT FOUND

{
  "detail": "Not found."
}
```

## Sobre Reviews:

Esse endpoint só poderá ser acesso por um usuário do tipo crítico, e será responsável por criar reviews baseado nos filmes na plataforma KMDb.

### `POST /api/movies/<int:movie_id>/review/` - Rota de criação de um review de um crítico

Agora que temos filmes cadastrados na plataforma, os críticos poderão realizar avaliações para eles.

**Importante!**

O campo stars aceita somente valores de 1 a 10.

```json
// REQUEST
// Header -> Authorization: Token <token-de-critic>
{
  "stars": 7,
  "review": "O Poderoso Chefão 2 podia ter dado muito errado...",
  "spoilers": false
}
```

```json
// RESPONSE STATUS 201 CREATED
{
  "id": 1,
  "critic": {
    "id": 1,
    "first_name": "Jacques",
    "last_name": "Aumont"
  },
  "stars": 7,
  "review": "O Poderoso Chefão 2 podia ter dado muito errado...",
  "spoilers": false
}
```

Caso o usuário crítico já tiver feito uma revisão para o filme especificado, deve retornar o status `HTTP - 422 UNPROCESSABLE ENTITY`.

```json
// RESPONSE STATUS -> HTTP 422 UNPROCESSABLE ENTITY
{
  "detail": "You already made this review."
}
```

Caso seja passado um `movie_id` inválido, deverá retornar um erro `HTTP 404 - NOT FOUND`.

```json
// RESPONSE STATUS -> HTTP 404 NOT FOUND
{
  "detail": "Not found."
}
```

Caso seja passado um valor para "stars" fora da faixa de 1 a 10, o sistema deverá ter o seguinte retorno:

```json
// RESPONSE STATUS -> HTTP 400 BAD REQUEST
// Caso seja passado um valor acima de 10
{
    "stars": [
        "Ensure this value is less than or equal to 10."
    ]

// Caso seja passado um valor abaixo de 1
{
    "stars": [
        "Ensure this value is greater than or equal to 1."
    ]
}
```

### `PUT /api/movies/<int:movie_id>/review/` - Rota que altera uma crítica já realizada

Não é necessário indicar o id da review a ser alterada, pois cada crítico só poderá ter uma crítica associada ao filme especificado.

```json
// REQUEST
// Header -> Authorization: Token <token-do-critic>
// Todos os campos são obrigatórios
{
  "stars": 2,
  "review": "O Poderoso Chefão 2 podia ter dado muito certo..",
  "spoilers": true
}
```

```json
//RESPONSE
{
  "id": 1,
  "critic": {
    "id": 1,
    "first_name": "Jacques",
    "last_name": "Aumont"
  },
  "stars": 2,
  "review": "O Poderoso Chefão 2 podia ter dado muito certo..",
  "spoilers": true
}
```

Caso seja passado um movie_id inválido ou o crítico tentar fazer uma alteração de uma avaliação de um filme que ele ainda não tenha feito, deverá retornar um erro `HTTP 404 - NOT FOUND`.

```json
// RESPONSE STATUS -> HTTP 404 NOT FOUND
{
  "detail": "Not found."
}
```

### `GET /api/reviews/` - Rota que lista as reviews que foram realizadas

Essa rota só pode ser acessada por um usuário do tipo critic ou admin.

Caso o usuário seja admin deve ser listada todas as reviews, caso seja um crítico deve listar apenas as críticas do próprio usuário.

```json
// REQUEST
// Header -> Authorization: Token <token-do-admin>

```

```json
// RESPONSE STATUS -> HTTP 200 OK
[
   {
      "id":1,
      "critic":{
         "id":1,
         "first_name":"Jacques",
         "last_name":"Aumont"
      },
      "stars":2,
      "review":"O Poderoso Chefão 2 podia ter dado muito certo..",
      "spoilers":true,
      "movie": 1
   },
   {
      "id":2,
      "critic":{
         "id":2,
         "first_name":"Bruce",
         "last_name":"Wayne"
      },
      "stars": 8,
      "review":"Não consegui ver até o final, fiquei com medo",
      "spoilers":false,
      "movie": 2
   },
   {
      "id":3,
      "critic":{
         "id":2,
         "first_name":"Bruce",
         "last_name":"Wayne"
      },
      "stars":10,
      "review":"Melhor filme que já assisti",
      "spoilers":true
      "movie": 1
   }
]

```

Perceba que foram listadas as todas as críticas de todos os usuários.

```json
// REQUEST
// Header -> Authorization: Token <token-do-critic>

```

```json
// RESPONSE STATUS -> HTTP 200 OK
[
  {
      "id":2,
      "critic":{
         "id":2,
         "first_name":"Bruce",
         "last_name":"Wayne"
      },
      "stars": 8,
      "review":"Não consegui ver até o final, fiquei com medo",
      "spoilers":false,
      "movie": 2
   },
   {
      "id":3,
      "critic":{
         "id":2,
         "first_name":"Bruce",
         "last_name":"Wayne"
      },
      "stars":10,
      "review":"Melhor filme que já assisti",
      "spoilers":true
      "movie": 1
   }
]

```

Nesse caso, apenas as críticas do crítico Bruce Wayne foram listadas.

## Tecnologias utilizadas 📱

- Django
- Django Rest Framework
- PostgreSQL
