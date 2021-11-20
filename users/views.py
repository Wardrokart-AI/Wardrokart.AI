# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages,auth
# from django.contrib.auth.models import User
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator
from django.contrib.auth import login
# from decorators import customer_required
from django.contrib.auth.decorators import login_required
import users.face_detect as face_detect
from users.models import Profile,User,UserUploads
from orders.models import Order
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from categories.models import Category
from django.shortcuts import get_object_or_404, redirect, render
from users.forms import SellerSignUpForm
import base64
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from django.core.files import File
from django.core.files.base import ContentFile
import requests
import os
from urllib.parse import urlparse
def register_customer(request):
	if request.user.is_authenticated == False:
		if request.method == 'POST':
			username = request.POST['username']
			email = request.POST['email']
			password = request.POST['password']
			password2 = request.POST['password2']
			latitude = request.POST['latitude']
			longitude = request.POST['longitude']
			location = request.POST['location']
			house = request.POST['house']

			img_encoded = request.POST['mydata']
			img_decode = base64.b64decode(img_encoded)


			if password == password2:
				if User.objects.filter(username=username).exists():
						messages.error(request , 'User Name Already Taken')
						return redirect('users:register')
				else:
					if User.objects.filter(email=email).exists():
						messages.error(request , 'Email Already Exits ')
						return redirect('users:register')
					else:
						user = User.objects.create_user(username=username,
														password=password,
														email=email,
														is_customer=True,
														latitude=latitude,
														longitude =longitude,
														location =location,
														office_name =house )

						Profile.objects.update_or_create(
							user=user,

						)
						user.save()
						profile = Profile.objects.get(user=user)
						profile.image = ContentFile(img_decode, 'profile.jpg')
						profile.save()
						messages.success(request,'You Are Now Registered')
						return redirect('users:login')
			else:
				messages.error(request , 'Password Doest Not Match')
				return redirect('users:register')

		else:
			return render(request,'users/register.html')
	else:
		messages.info(request , 'You Are Already Logged In')
		return redirect('users:dashboard')

def login_customer(request):
	if request.user.is_authenticated == False:
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']

			user = auth.authenticate(username=username , password=password)

			if(User.objects.filter(username = username)):
				if(User.objects.filter(username = username).values("is_customer")):
					if(User.objects.filter(username = username).values("is_customer")[0]):
						is_customer = User.objects.filter(username = username).values("is_customer")[0]["is_customer"]
			if(User.objects.filter(username = username)):
				if(User.objects.filter(username = username).values("is_seller")):
					if(User.objects.filter(username = username).values("is_seller")[0]):
						is_seller = User.objects.filter(username = username).values("is_seller")[0]["is_seller"]
			# is_seller = User.objects.filter(username = username).values("is_seller")[0]["is_seller"]

			if user is not None and is_customer:
				res = face_detect.check(user)
				res = True
				if res:
					auth.login(request,user)
					messages.success(request,'You Are Now LoggedIn')
					return redirect('users:dashboard')
				messages.error(request,'Unauthorized access')
				return render(request,'users/login.html')


			elif user is not None and is_seller:
				res = face_detect.check(user)
				res = True
				if res:
					auth.login(request,user)
					messages.success(request,'You Are Now LoggedIn')
					return redirect('users:home')
				messages.error(request,'Unauthorized access')
				return render(request,'users/login.html')
			else:
				messages.error(request,'Invalid Credentials')
				return redirect('users:login')

		else:
			return render(request,'users/login.html')

	else:
		messages.error(request,'You Are Alredy Logged In')
		return redirect('users:dashboard')



@login_required(login_url="/users/login")
def dashboard_customer(request):
	print("DASHBOARD PRINTING")
	orders = Order.objects.filter(user_id=request.user.id)
	print(orders)
	context = {
		'title': request.user.username + ' Shopping Details',
		'orders': orders
	}
	return render(request,'users/dashboard.html',context)



@login_required(login_url="/users/login")
def profile_customer(request,user_id):
	if request.method == 'POST':
		try:
			image = request.FILES['image']
		except MultiValueDictKeyError:
			image = False
		title = request.POST['title']
		user = get_object_or_404(User,pk=user_id)
		
		
		if image == False:
			return redirect('users:profile',user_id = user_id)
		else:
			cat = UserUploads.objects.create(
						user = user,
						title=title,
						photo=image
					)

			cat.save()
			print("UserUploads")
			messages.success(request,'Image Added to Profile SuccessFully')
			return redirect('users:profile',user_id = user_id)
	else:
		if(request.user.is_customer):
			user_id = request.user.id
			products = UserUploads.objects.filter(user=user_id)

			context = {

				# 'title':request.user.name,
				'products':products,
			}
			return render(request ,'users/profile.html' , context)

		return render(request,'users/profile.html')

@login_required(login_url="/users/login")
def logout_customer(request):
	if request.method == 'POST':
		auth.logout(request)
		messages.success(request,'You Are Now Logged Out')
		return redirect('pages:home')


