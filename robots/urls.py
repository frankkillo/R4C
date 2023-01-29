from django.urls import path

from .views import create_robot, read_robots_xlsx


urlpatterns = [
    path('robots/', create_robot, name="api-robots-create"),
    path('robots/xlsx/', read_robots_xlsx, name="robots-xlsx"),
]