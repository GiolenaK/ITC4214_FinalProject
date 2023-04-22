from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('collections/', views.CollectionListView.as_view(), name='collection_list'),
    path('home/', views.product_list, name='store_home'),
    path('about/', views.store_about, name='store_about'),

]