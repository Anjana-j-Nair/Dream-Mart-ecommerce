from django.shortcuts import get_object_or_404, redirect, render
from ecommerceapp.models import Product
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,p_id):
    product=Product.objects.get(id=p_id)
    try:
        cart=Cart.objects.get(c_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(c_id=_cart_id(request))
        cart.save()
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(product=product,quantity=1,cart=cart)
        cart_item.save()
    return redirect('cartapp:cart_detail')

def cart_detail(request,total=0,counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(c_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for c in cart_items:
            total +=(c.product.price*c.quantity)
            counter +=c.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',dict(cart_item=cart_items,Total=total,counter=counter))

def cart_remove(request,p_id):
    cart=Cart.objects.get(c_id=_cart_id(request))
    product=get_object_or_404(Product,id=p_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cartapp:cart_detail')

def full_delete(request,p_id):
    cart=Cart.objects.get(c_id=_cart_id(request))
    product=get_object_or_404(Product,id=p_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cartapp:cart_detail')