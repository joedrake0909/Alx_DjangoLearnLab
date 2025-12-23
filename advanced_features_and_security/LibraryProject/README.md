# LibraryProject

A Django web application for library management.

## Setup Instructions

### Prerequisites
- Python 3.x
- pip package manager

### Installation

1. **Install Django**
   ```bash
   pip install django
   ```

2. **Create Project**
   ```bash
   django-admin startproject LibraryProject
   cd LibraryProject
   ```

3. **Run Server**
   ```bash
   python manage.py runserver
   ```

4. **View Application**
   - Open browser and go to: `http://127.0.0.1:8000/`
   - You should see the Django welcome page

## Project Structure

```
LibraryProject/
├── manage.py
└── LibraryProject/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

### Key Files
- **manage.py**: Command-line utility for project management
- **settings.py**: Project configuration and settings
- **urls.py**: URL routing definitions

## Development Status
🚧 Project is in initial setup phase. More features coming soon!