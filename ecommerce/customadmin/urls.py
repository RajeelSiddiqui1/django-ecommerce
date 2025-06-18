from django.urls import path
from . import views

urlpatterns = [
    # admin actions
    path('dashboard', views.dashboard, name='dashboard'),
    # path('admin/signup/', views.admin_signup, name='admin_signup'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    #catregory
    path('category/list/', views.list_category, name='category_list'),
    path('category/create/', views.create_category, name='category_create'),
    path('<int:cat_id>/category/edit/', views.edit_category, name='category_edit'),
    path('<int:cat_id>/category/delete/', views.delete_category, name='category_delete'),
    #products
    path('product/list', views.product_list, name='product_list'),
    path('product/craete', views.craete_product, name='create_product'),
    path('<int:product_id>/product/edit', views.edit_product, name='edit_product'),
    path('<int:product_id>/product/delete', views.delete_product, name='delete_product'),
    path('orders/', views.admin_order_history, name='admin_order_history'),
    path('admin/order/<int:order_id>/<str:action>/', views.admin_update_order_status, name='admin_update_order_status'),
    path('userlist/', views.user_list, name='user_list'),
]
