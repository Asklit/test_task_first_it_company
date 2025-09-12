# Веб-сервис для управления движением денежных средств (ДДС) с полной Docker-интеграцией.

## Built With

- [Django](https://www.djangoproject.com/) - Backend framework
- [Django REST Framework](https://www.django-rest-framework.org/) - API framework
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Docker](https://www.docker.com/) - Containerization
- [Docker Compose](https://docs.docker.com/compose/) - Multi-container orchestration

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Ensure ports `80`, `8000`, and `5432` are free

## Installation

1. Clone the repo
   ```bash
   git clone github.com/Asklit/test_task_first_it_company
   cd test_task_first_it_company
   ```
2. Create environment file
   ```bash
   cp .env.test .env
   ```
3. Build and start containers
   ```bash
   docker-compose up --build
   ```
4. Apply database migrations
   ```bash
   docker-compose exec backend python manage.py migrate
   ```
5. Create superuser
   
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```
6. Use link to access admin panel
   
     Django Admin url: localhost/admin


## Run tests

   ``` 
   docker-compose exec backend pytest transactions/tests/ -v 
   ```
