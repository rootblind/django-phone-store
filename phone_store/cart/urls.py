from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path("", views.cart, name='cart'),
    path("add-to-cart/<int:pk>", views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment_success/", views.payment_success, name="payment_success"),
]