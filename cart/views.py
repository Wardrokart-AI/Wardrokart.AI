import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from products.models import Product
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
from django.views.decorators.http import require_POST
from .cart import Cart
from django.core.mail import send_mail
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url="/users/login")
def cart_add(request, product_productid):
	cart = Cart(request)
	product = Product.objects.get(productid=product_productid)
	qty = product.quantity
	product.quantity = qty-1
	product.save()
	cart.add(product=product)
	return redirect('/shop/')



