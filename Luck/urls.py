from django.urls import path
from .views import luck_page

urlpatterns = [
    path('', luck_page),
]