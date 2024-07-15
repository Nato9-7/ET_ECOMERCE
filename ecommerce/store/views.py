from django.shortcuts import render
from .models import Product, Category
from django.db import connection

def home(request):
    toys_category = Category.objects.get(name='juguete')
    meats_category = Category.objects.get(name='carne')
    bebida_category = Category.objects.get(name='bebida')
    lacteo_category = Category.objects.get(name='lacteo')
    snak_category = Category.objects.get(name='snak')
    # Filtrar productos por categoría
    toys_products = Product.objects.filter(category = toys_category)
    meats_products = Product.objects.filter(category = meats_category)
    bebida_products = Product.objects.filter(category = bebida_category)
    lacteo_products = Product.objects.filter(category = lacteo_category)
    snak_products = Product.objects.filter(category = snak_category)
    return render(request, 'index.html', {
        'toys_products': toys_products,
        'meats_products': meats_products,
        'lacteo_products': lacteo_products,
        'snak_products': snak_products,
        'bebida_products': bebida_products
    })

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def raw_product_list(request):
    productos =  Product.objects.filter(category = 3)
    return render(request, "raw_product_list.html", {"productos" : productos})

