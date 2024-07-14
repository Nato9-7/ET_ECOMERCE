from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product_list', views.product_list, name='product_list'),
    path('raw/', views.raw_product_list, name='raw_product_list'),
]

