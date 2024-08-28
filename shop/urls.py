from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.handle_post_request, name='product_create'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/', views.product_list, name='product_list'),
]
