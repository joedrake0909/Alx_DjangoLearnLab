from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', include('relationship_app.urls', namespace="relationship_app")),  # ← CORRECT
]
=======
    path('', include('relationship_app.urls'), namespace="relationship_app"),  # Include app URLs
]
>>>>>>> 334fe33c6989c2809a74e13e3f924dc8223f1f45
