from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db import connection

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products[:6]})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'producto.html', {'product': product})

def raw_product_list(request):

    # products = Product.objects.all()
    # raw_products = Product.objects.all()  # Supongamos que tienes otro modelo llamado RawProduct
    # context = {
    #     'products': products,
    #     'raw_products': raw_products,
    # }
    # return render(request, 'index.html', context)


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


