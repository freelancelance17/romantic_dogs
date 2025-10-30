from django.urls import path
from .views import default

urlpatterns = [
    path("", default),
]
