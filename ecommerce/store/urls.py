from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('producto/<int:pk>/', views.product_detail, name='producto'),
    path('raw/', views.raw_product_list, name='raw_product_list'),
]

