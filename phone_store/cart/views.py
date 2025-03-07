from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from item.models import Cart, CartItem, item
from .forms import PaymentForm

@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            cart_item.total_price = cart_item.item.price * cart_item.quantity
    else:
        cart_items = []

    total_price = sum(cart_item.item.price * cart_item.quantity for cart_item in cart_items)

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(item, pk=pk)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} was added to your cart!")

    return redirect("cart:cart")

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(cart_item.item.price * cart_item.quantity for cart_item in cart_items)

    if request.method == "POST":
        form = PaymentForm(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.payment_value = total_price
            payment.user = request.user
            payment.save()

            return redirect('cart:payment_success')
        
    else:
        form = PaymentForm()
    
    return render(request, 'cart/checkout.html', {
        'total_price': total_price,
        'cart': cart,
        'cart_items': cart_items,
        'form': form
    })

def payment_success(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.cart_items.all().delete()
        cart.delete()

    messages.success(request, "Your order has been successfully placed!")
    return render(request, "cart/payment_success.html")