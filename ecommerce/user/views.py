from django.shortcuts import render, redirect, get_object_or_404
from customadmin.models import Category, Products
from .models import SimpleUser, CartItem, Order, OrderItem
from .forms import UserRegisterForm, UserLoginForm, CheckoutForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.http import JsonResponse

def register(request):
    if request.session.get('user_logged_in'):
        messages.success(request, 'You are already logged in.')
        return redirect('home_page')
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Register successfully completed')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.session.get('user_logged_in'):
        messages.warning(request, 'You are already logged in.')
        return redirect('home_page')
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = SimpleUser.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_logged_in'] = True
                    request.session['user_name'] = user.name
                    request.session['user_id'] = user.id
                    messages.success(request, 'Login successfully completed')
                    return redirect('home_page')
            except SimpleUser.DoesNotExist:
                messages.error(request, 'Invalid credentials')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successfuly')
    return redirect('home_page')

def home_page(request):
    categories = Category.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'categories': categories})

def products(request, cat_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to see products.")
        return redirect('home_page')
    else:
        category = get_object_or_404(Category, pk=cat_id)
        products = Products.objects.filter(categories=category)
        return render(request, 'products.html', {'products': products})
    

def all_products(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to see product detail.")
        return redirect('home_page')
    products = Products.objects.all()
    return render(request, 'all_products.html', {'products': products})

def product_detail(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to see product detail.")
        return redirect('home_page')
    product = get_object_or_404(Products, pk=product_id)
    related_products = Products.objects.filter(categories=product.categories).exclude(pk=product_id)[:3]
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products
    })

def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def cart_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = get_object_or_404(SimpleUser, id=user_id)
        cart_items = CartItem.objects.filter(user=user)
    else:
        cart_items = CartItem.objects.filter(session_key=get_session_key(request))
    total = sum(item.total_price for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    user_id = request.session.get('user_id')
    if user_id:
        user = get_object_or_404(SimpleUser, id=user_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': 1}
        )
    else:
        session_key = get_session_key(request)
        cart_item, created = CartItem.objects.get_or_create(
            session_key=session_key,
            product=product,
            defaults={'quantity': 1}
        )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart!")
    return redirect('cart_view')


def increase_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    item.quantity +=1
    item.save()
    messages.info(request, 'Item add successfully')
    return redirect('cart_view')

def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    messages.info(request, 'Item add successfully')
    return redirect('cart_view') 

def remove_from_cart(request, item_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to remove items from the cart.")
        return redirect('login')
    user = get_object_or_404(SimpleUser, id=user_id)
    cart_item = get_object_or_404(CartItem, id=item_id, user=user)
    cart_item.delete()
    messages.success(request, "Item removed from cart!")
    return redirect('cart_view')

def checkout_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to proceed to checkout.")
        return redirect('login')
    user = get_object_or_404(SimpleUser, id=user_id)
    cart_items = CartItem.objects.filter(user=user)
    if not cart_items:
        messages.warning(request, "Your cart is empty!")
        return redirect('cart_view')
    total = sum(item.total_price for item in cart_items)
    form = CheckoutForm()
    context = {
        'cart_items': cart_items,
        'total': total,
        'form': form,
    }
    return render(request, 'checkout.html', context)

def process_order(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to place an order.")
        return redirect('login')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(SimpleUser, id=user_id)
            cart_items = CartItem.objects.filter(user=user)
            if not cart_items:
                messages.warning(request, "Your cart is empty!")
                return redirect('cart_view')
            total = sum(item.total_price for item in cart_items)
            order = form.save(commit=False)
            order.user = user
            order.total = total
            order.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.total_price
                )
            cart_items.delete()
            messages.success(request, "Order placed successfully!")
            return redirect('cart_view')
    return redirect('checkout_view')


def order_history(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to view order history.")
        return redirect('login')
    user = get_object_or_404(SimpleUser, id=user_id)
    orders = Order.objects.filter(user=user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'order_history.html', context)

def order_detail(request, order_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to view order details.")
        return redirect('login')
    user = get_object_or_404(SimpleUser, id=user_id)
    order = get_object_or_404(Order, id=order_id, user=user)
    order_items = order.items.all()
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order_detail.html', context)