# Controle de Progressão de Carga de Academia e Evolução

Este é um projeto em Django de uma API para controlar a progressão de carga em exercícios de academia e acompanhar a evolução dos usuários.

## Requisitos do sistema

- Linux
- Python >= 3.8
- Django

## Configuração do ambiente de desenvolvimento

Não há instruções específicas de configuração do ambiente de desenvolvimento.

## Dependências

As dependências necessárias para executar o projeto estão listadas no arquivo `requirements.txt`.

Para instalá-las, execute o seguinte comando:

pip install -r requirements.txt

## Executando o projeto localmente

Para executar o projeto localmente, siga as etapas abaixo:

1. Crie um ambiente virtual:

python -m venv myenv

2. Ative o ambiente virtual:

source myenv/bin/activate

3. Instale as dependências:

4. Execute o servidor de desenvolvimento:

python manage.py runserver

## Endpoints/APIs

Todos os endpoints/APIs disponíveis podem ser acessados através do Swagger, acessível na rota `/api/docs`.

## Modelos de Dados

O projeto utiliza os seguintes modelos de dados:

- Exercise (Exercício)
- Progression (Progressão)

## Autenticação

Para autenticar-se na API e obter um token de acesso, faça uma requisição POST para `/api/token/pair`, fornecendo um email e uma senha válidos.

Exemplo de requisição usando cURL:

curl -X 'POST'
'https://gym-weight-tracker.vercel.app/api/token/pair'
-H 'accept: application/json'
-H 'Content-Type: application/json'
-d '{
"password": "pass",
"email": "email"
}'

## Formatos de Dados

A API suporta o formato de dados JSON.

## Contribuição

Não existem instruções específicas para contribuição no momento.

## Testes

O projeto não possui testes automatizados.

## Práticas Recomendadas

Não existem práticas recomendadas específicas no momento.

## Exemplo de Uso

Você pode consultar o Swagger para obter exemplos de uso e entender como utilizar a API.

## Mantenedor

Este projeto é mantido por Pedro Barbosa.

- Email: pedrohsbarbosa99@gmail.com
- GitHub: [pedrohsbarbosa99](https://github.com/pedrohsbarbosa99)

Sinta-se à vontade para entrar em contato com o mantenedor para obter mais informações ou esclarecer dúvidas sobre o projeto.

Este é um projeto pessoal com o intuito de estudo.
