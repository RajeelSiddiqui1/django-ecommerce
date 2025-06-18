from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('all_products/', views.all_products, name="all_products"),
    path('<int:cat_id>products/', views.products, name="products"),
    path('products/<int:product_id>/detail/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:item_id>/', views.increase_item, name='increase_item'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('process-order/', views.process_order, name='process_order'),
    path('order-history/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
