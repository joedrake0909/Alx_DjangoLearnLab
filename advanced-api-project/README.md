# Advanced API Project

This Django project demonstrates advanced API development using Django REST Framework with custom serializers, nested relationships, and data validation.

## Features
- Custom serializers for complex data structures
- Nested object serialization
- Custom validation logic
- Author-Book relationship management

## Setup
1. Install dependencies: `pip install django djangorestframework`
2. Run migrations: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`
4. Run server: `python manage.py runserver`

## Models
- **Author**: Represents book authors with a name field
- **Book**: Represents books with title, publication_year, and foreign key to Author

## Testing
Use Django admin or Django shell to test the API functionality.
