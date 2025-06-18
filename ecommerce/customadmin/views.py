from django.shortcuts import render
from . models import Category, Admin, Products
from . forms import CategoryForm, AdminSignup, AdminLoginForm, ProductForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from user.models import Order, SimpleUser

#dashboard
def dashboard(request):
   return render(request, 'dashboard.html')

#admin signup
def admin_signup(request):
   if request.method == "POST":
      form = AdminSignup(request.POST)
      if form.is_valid():
         form.save()
         return redirect('admin_login')
   else:
       form = AdminSignup()
       return render(request, 'admin_signup.html', {'form': form})   
   
#admin login
def admin_login(request):
   if request.method == "POST":
      form =AdminLoginForm(request.POST)
      if form.is_valid():
         email = form.cleaned_data['email']
         password = form.cleaned_data['password']
         try:
            admin = Admin.objects.get(email=email)
            if check_password(password, admin.password):
               request.session['admin_logged_in'] = True
               request.session['admin_name'] = admin.name
               request.session['admin_id'] = admin.id
               return redirect('dashboard')
            messages.error(request, 'Invalid credentials')
         except Admin.DoesNotExist:
             messages.error(request, 'Invalid credentials')

   else:          
      form = AdminLoginForm()
   return render(request, 'admin_login.html', {'form':form})   

#admin logout
def admin_logout(request):
   logout(request)
   return redirect('dashboard')

#list category
def list_category(request):
   category = Category.objects.all().order_by('-created_at')
   return render(request, 'category_list.html', {'category':category})


def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            messages.success(request, 'Category has been uploaded successfully!', extra_tags='alert-success')
            return redirect('category_list')
        else:
            messages.error(request, 'Form is not valid.', extra_tags='alert-danger')
    else:
        form = CategoryForm()
    
    return render(request, 'category_form.html', {'form': form})


# edit Category
def edit_category(request, cat_id):
   category = get_object_or_404(Category, pk=cat_id)
   if request.method == "POST":
      form = CategoryForm(request.POST, request.FILES, instance=category)
      if form.is_valid():
         category = form.save(commit=False)
         category.save()
         messages.success(request, 'Category has been updated')
         return redirect('category_list')
      else:
           return ValueError(request, 'Category update to feild') 

   else:
      form = CategoryForm(instance=category)

   return render(request, 'category_form.html',{'form':form})   
   
#delete category
def delete_category(request, cat_id):
   category = get_object_or_404(Category, pk=cat_id)
   if request.method == "POST":
    category.delete()
    messages.success(request, 'Category has been delted')
    return redirect('category_list')
   else:
      return render(request, 'delete_category.html',{'category':category})    
   
# product list 
def product_list(request):
   products = Products.objects.all().order_by('-created_at')
   return render(request, 'product_list.html',{'products': products})

#product craete
def craete_product(request):
   if request.method == "POST":
      form = ProductForm(request.POST, request.FILES)
      if form.is_valid():
         form.save(commit=False)
         form.save()
         messages.success(request,'Product has been uploaded successfully',
         extra_tags='alret-success')
         return redirect('product_list')
      else:
         return ValueError(request, 'Product upload to feild') 
   else:
      form = ProductForm()
   return render(request, 'product_form.html', {'form':form})   

# def product_status(request):
#     products = Products.objects.filter(is_delete=False)
    
#     if request.method == "POST":
#         product_id = request.POST.get('product_id')
#         if not product_id:
#             messages.error(request, 'No Product has been found')
#             return redirect('product_list')

#         product = get_object_or_404(Products, pk=product_id)
#         status_form = ProductStatusForm(request.POST)
#         if status_form.is_valid():
#             action = status_form.cleaned_data['action']
#             product.status = action
#             product.save()
#             messages.success(request, f'Product status updated to {action}')
#             return redirect('product_list')
#         else:
#             messages.error(request, 'Invalid form submission')

#     # Create a list of products with their respective forms
#     product_list = [
#         {
#             'product': product,
#             'status_form': ProductStatusForm(initial={'action': product.status})
#         }
#         for product in products
#     ]

#     return render(request, 'product_list.html', {
#         'product_list': product_list,
#     })

# product edit 
def edit_product(request, product_id):
   prodcts = get_object_or_404(Products, pk=product_id)
   if request.method == "POST":
      form = ProductForm(request.POST, request.FILES, instance=prodcts)
      if form.is_valid():
         form.save()
         messages.success(request,"Product has been updated successfully", extra_tags='alret-success')
      return redirect('product_list')
   else:
      form = ProductForm(instance=prodcts)
   return render(request, 'product_form.html', {'form':form})

# product delete
def delete_product(request, product_id):
   product = get_object_or_404(Products, pk=product_id)
   if request.method == "POST":
      product.delete()
      messages.success(request, 'Category has been delted')
      return redirect('product_list')
   else:
      return render(request, 'delete_product.html',{'product':product})    
   
   
def admin_order_history(request):

    
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = Order.objects.filter(status=status_filter).order_by('-created_at')
    else:
        orders = Order.objects.all().order_by('-created_at')
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'admin_order_history.html', context)

def admin_update_order_status(request, order_id, action):

    
    order = get_object_or_404(Order, id=order_id)
    if action == 'confirm':
        order.status = 'Confirmed'
        messages.success(request, f"Order #{order.id} confirmed successfully.")
    elif action == 'reject':
        order.status = 'Rejected'
        messages.success(request, f"Order #{order.id} rejected successfully.")
    order.save()
    
    return redirect('admin_order_history')   
    
    
def user_list(request):
       users = SimpleUser.objects.all()
       return render(request,'user_list.html',{'users':users})