import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from products.models import Product
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
from django.views.decorators.http import require_POST
from .cart import Cart
from orders.models import Order
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

# @login_required(login_url="/users/login")
# def cart_detail(request):
# 	sub = []
# 	qty = []
# 	total = 0
# 	for key,value in request.session['cart'].items():
# 		sub.append(float(value['price']) * float(value['quantity']))
# 		qty.append(int(value['quantity']))
# 	for s in sub:
# 		total = total + s
# 	context = {
#     	'title' : 'My Cart',
#     	'sub' : sub,
#     	'total' : total
#     }
# 	return render(request,'cart/cart_detail.html',context)
@login_required(login_url="/users/login")
def cart_detail(request):
	sub = []
	qty = []
	total = 0
	if('cart' in request.session):
		for key,value in request.session['cart'].items():
			sub.append(float(value['price']) * float(value['quantity']))
			qty.append(int(value['quantity']))
		for s in sub:
			total = total + s
		context = {
			'title' : 'My Cart',
			'sub' : sub,
			'total' : total
		}
		return render(request,'cart/cart_detail.html',context)
	else:
		return redirect('/shop')

@login_required(login_url="/users/login")
def item_clear(request,product_productid):
	cart = Cart(request)
	product = Product.objects.get(productid=product_productid)
	qty = product.quantity
	for key,value in request.session['cart'].items():
		if value['productid']==product_productid:
			product.quantity = qty+value['quantity']
			break
	product.save()
	cart.remove(product)
	return redirect('cart:cart_detail')

@login_required(login_url="/users/login")
def item_increment(request,product_productid):
	cart = Cart(request)
	product = Product.objects.get(productid=product_productid)
	qty = product.quantity
	if qty>0:

		for key,value in request.session['cart'].items():
			if value['productid']==product_productid:
				product.quantity = qty-1
				break
		product.save()
		cart.add(product=product)
		return redirect('cart:cart_detail')
	else:
		messages.info(request,"No more product in the stock!")
		return redirect('cart:cart_detail')


@login_required(login_url="/users/login")
def item_decrement(request,product_productid):
	cart = Cart(request)
	product = Product.objects.get(productid=product_productid)
	qty = product.quantity
	for key,value in request.session['cart'].items():
		if value['productid']==product_productid:
			product.quantity = qty+1
			break
	cart.decrement(product=product)
	product.save()
	return redirect('cart:cart_detail')

@login_required(login_url="/users/login")
def cart_clear(request):
	cart = Cart(request)
	qty=[]
	pid = []
	for key,value in request.session['cart'].items():
		qty.append(value['quantity'])
		pid.append(value['productid'])
	for i in range(len(pid)):
		product = Product.objects.get(productid=pid[i])
		q = product.quantity
		product.quantity = q+qty[i]
		product.save()
	cart.clear()
	return redirect('cart:cart_detail')

@login_required(login_url="/users/login")
def checkout(request):
	sub = []
	qty = []
	total = 0
	if len(request.session['cart']) != 0:
		for key,value in request.session['cart'].items():
			sub.append(float(value['price']) * float(value['quantity']))
			qty.append(int(value['quantity']))
		for s in sub:
			total = total + s
		context = {
	    	'title' : 'CheckOut',
	    	'sub' : sub,
	    	'total' : total
	    }
		return render(request,'cart/checkout.html',context)
	else:
		messages.info(request,"Your cart Is Empty")
		return redirect('/')

