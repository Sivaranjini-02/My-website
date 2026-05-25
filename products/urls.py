from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.index, name='index'),
    path('cart/', views.view_cart, name='view_cart'),
    path('signup/', views.signup, name='signup'),
    path('checkout/', views.checkout, name='checkout'),
    path('api/catalog/', views.api_product_list, name='api_product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('orders/', views.order_tracking, name='order_tracking'),
]