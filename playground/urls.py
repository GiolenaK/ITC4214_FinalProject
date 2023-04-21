from django.urls import path
from . import views

urlpatterns = [
    path('', views.playground_home, name='playground_home'),
]