# Gym Weight Progress and Evolution Control

## Frameworks

<img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/>
<img src="https://cdn.worldvectorlogo.com/logos/cockroachdb.svg" alt="cockroachdb" width="40" height="40"/>

##

This is a Django project for an API that controls weight progression in gym exercises and tracks users' evolution.

## System Requirements

- Linux
- Python >= 3.8

## Development Environment Setup

There are no specific instructions for setting up the development environment.

## Dependencies

The dependencies required to run the project are listed in the `requirements.txt` file.

To install them, run the following command:

pip install -r requirements.txt

## Running the Project Locally

To run the project locally, follow the steps below:

1. Create a virtual environment:

python -m venv myenv

2. Activate the virtual environment:

source myenv/bin/activate

3. Install the dependencies:

pip install -r requirements-dev.txt && pre-commit install

4. Create .env

python contrib/env_gen.py

5. Create postgres db and loaddata

docker-compose up db
./manage.py loaddata contrib/db_data.json

6. Run the development server:

python manage.py runserver

## Endpoints/APIs

All available endpoints/APIs can be accessed through Swagger, accessible at `/api/docs`.

## Data Models

The project uses the following data models:

- Exercise
- Progression

## Authentication

To authenticate to the API and obtain an access token, make a POST request to `/api/token/pair`, providing a valid email and password.

Example request using cURL:

curl -X 'POST'
'http://127.0.0.1:8000/api/token/pair'
-H 'accept: application/json'
-H 'Content-Type: application/json'
-d '{
"password": "pass",
"email": "email"
}'

## Data Formats

The API supports JSON data format.

## Contribution

There are no specific instructions for contribution at the moment.

## Testing

The project does not have automated tests.

## Best Practices

There are no specific recommended best practices at the moment.

## Example Usage

You can refer to Swagger for usage examples and understanding how to utilize the API.

## Maintainer

This project is maintained by Pedro Barbosa.

- Email: pedrohsbarbosa99@gmail.com
- GitHub: [pedrohsbarbosa99](https://github.com/pedrohsbarbosa99)

Feel free to contact the maintainer for more information or clarification regarding the project.

This is a personal project intended for study purposes.
