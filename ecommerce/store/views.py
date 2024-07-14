from django.shortcuts import render
from .models import Product
from django.db import connection

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def raw_product_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM store_product")
        products = cursor.fetchall()
    return render(request, 'raw_product_list.html', {'products': products})

