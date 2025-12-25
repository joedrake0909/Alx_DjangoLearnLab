from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls', namespace="relationship_app")),
    path('bookshelf/', include(('bookshelf.urls', 'bookshelf'), namespace='bookshelf')),
]