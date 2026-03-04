from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    # Add this new line right here:
    path('add/', views.add_product, name='add_product'), 
]