# Web service for cash flow Management (DDS) with full Docker integration.

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
   git clone https://github.com/Asklit/test_task_first_it_company
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
   
     http://localhost:8000/admin/


## Run tests with active docker container

   ``` 
   docker-compose exec backend pytest core/tests/ -v 
   ```
## Core Entities

### `Status`
- **Purpose**: Defines transaction statuses (Business, Personal, Tax, etc.)
- **Fields**: 
  - `name` - Unique status identifier (max 30 chars)

### `TransactionType`
- **Purpose**: Categorizes transactions (Income, Expense)
- **Fields**:
  - `name` - Unique type name (max 30 chars)

### `Category`
- **Purpose**: Groups transactions under specific types
- **Fields**:
  - `name` - Unique category name (max 30 chars)
  - `root_transaction_type` - ForeignKey to TransactionType

### `Subcategory`
- **Purpose**: Provides detailed classification within categories
- **Fields**:
  - `name` - Unique subcategory name (max 30 chars)
  - `root_category` - ForeignKey to Category

### `Transaction`
- **Purpose**: Main financial transaction record
- **Fields**:
  - `create_date` - Auto-set to current date (editable)
  - `status` - ForeignKey to Status
  - `transaction_type` - ForeignKey to TransactionType
  - `category` - ForeignKey to Category
  - `subcategory` - ForeignKey to Subcategory
  - `amount` - Decimal value (min 0.01)
  - `notes` - Optional comments (max 100 chars)
