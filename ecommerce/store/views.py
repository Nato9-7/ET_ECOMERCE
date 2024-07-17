from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, CartItem, Cart
from .forms import AddToCartForm
from django.db import connection
from django.urls import reverse
from django.db.models import Q

@login_required
def home(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.all()  
    form = AddToCartForm()
    search_query = request.GET.get('q')

    if search_query:
        product = product.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            return redirect('product_detail', pk=product_id)
    
    context = {
        'product': product[:6],
        'cart': cart,
        'form': form,
        'search_query': search_query,
    }
    return render(request, 'index.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_list = Product.objects.all()  

    cart, created = Cart.objects.get_or_create(user=request.user)
    form = AddToCartForm()
    
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            # Redirect to avoid form resubmission on refresh
            return redirect('lista_productos')
    
    context = {
     'product': product,
     'product_list': product_list [:6],
     'cart': cart,
     'form': form,
     }

    return render(request, 'producto.html', context)

def raw_product_list(request):
    category_id = request.GET.get('category')
    products = Product.objects.all()
    cart, created = Cart.objects.get_or_create(user=request.user)
    form = AddToCartForm()

    if category_id:
        products = products.filter(category_id=category_id)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            # Redirect to avoid form resubmission on refresh
            return redirect('lista_productos')

    context = {
        'products': products,
        'cart': cart,
        'form': form,
        'active_category': category_id  # Pasar el ID de la categoría activa al contexto
    }
    return render(request, 'lista_productos.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    referer = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            # Verificar si el producto ya está en el carrito
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity  # Sumar la cantidad nueva a la existente
            cart_item.save()

            # Redireccionar a la página anterior si existe
            if referer:
                return HttpResponseRedirect(referer)
            else:
                return redirect('cart_detail')
    else:
        form = AddToCartForm()

    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'product.html', context)

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    referer = request.META.get('HTTP_REFERER')
    # return render(request, 'index.html', {'cart': cart})
    if referer:
        return HttpResponseRedirect(referer)
    else:
        return HttpResponseRedirect(reverse('cart_summary'))


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return HttpResponseRedirect(referer)
    else:
        return HttpResponseRedirect(reverse('cart_summary'))



def cart_summary(request):
     # Obtener el carrito del usuario actual
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Obtener todos los items del carrito
    cart_items = cart.cartitem_set.all()

    # Calcular el precio total del carrito
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Renderizar el template con el contexto 
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'carrito.html', context)


def search_redirect(request):
    search_query = request.GET.get('q')
    if search_query:
        # Busca productos que coincidan con el nombre o la descripción
        product = Product.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query)).first()
        
        # Si encuentra un producto, redirige a la página de detalle del producto
        if product:
            return redirect('producto', pk=product.pk)
        
        # Si no encuentra un producto, busca una categoría que coincida con el nombre
        category = Category.objects.filter(name__icontains=search_query).first()
        if category:
            return redirect(f'{reverse("lista_productos")}?category={category.id}')
        
        # Si no encuentra ni producto ni categoría, redirige a la página principal
        return redirect('home')
    return redirect('home')