from django.urls import path
from . import views

urlpatterns = [
    path('', views.playground_home, name='playground_home'),
    path('about/', views.playground_about, name='playground_about'),
]