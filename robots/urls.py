from django.urls import path

from .views import create_robot


urlpatterns = [
    path('robots/', create_robot, name="api-robots-create"),
]