"""
URL configuration for advanced_api_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# ==================== MAIN URL CONFIGURATION ====================
# This is the root URL configuration for the project.
# It includes the Django admin interface and the API endpoints.

urlpatterns = [
    # Django Admin Interface
    # URL: /admin/
    # Provides access to the Django administration panel
    path('admin/', admin.site.urls),
    
    # API Endpoints
    # URL: /api/
    # Includes all API-related URLs from the api app
    # This provides access to:
    # - GET /api/books/ - List all books
    # - GET /api/books/<id>/ - Get book details
    # - POST /api/books/create/ - Create new book (auth required)
    # - PUT/PATCH /api/books/<id>/update/ - Update book (auth required)
    # - DELETE /api/books/<id>/delete/ - Delete book (auth required)
    path('api/', include('api.urls')),
]

# ==================== URL CONFIGURATION NOTES ====================
#
# URL Prefixes:
# - /admin/ - Django admin panel
# - /api/ - All API endpoints
#
# The 'api/' prefix keeps API endpoints separate from other parts of the application
# and provides a clear, RESTful URL structure.
#
# To access the API:
# - Development: http://localhost:8000/api/books/
# - Production: https://yourdomain.com/api/books/
#
# Django REST Framework Browsable API:
# When you visit these URLs in a browser while logged in, DRF provides
# a browsable HTML interface for testing API endpoints.
