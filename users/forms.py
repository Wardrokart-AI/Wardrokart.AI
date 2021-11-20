from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from users.models import (User)


class SellerSignUpForm(UserCreationForm):
    username = forms.CharField(label='Username' , widget=forms.TextInput(attrs={'class':'form-control','required':True}), error_messages={'required': 'Please enter valid username','unique':'User Already Exists'})
    email = forms.EmailField(label='Email Address',widget=forms.EmailInput(attrs={'class':'form-control'}),error_messages={'required': 'Email Address Required','unique':'Email Already Exists'})
    password1 = forms.CharField(label='Password' ,widget=forms.PasswordInput(attrs={'class':'form-control'}),error_messages={'required': 'Password Required','password_mismatch':'Passwords Do not Match!!'})
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}),error_messages={'required': 'Password Required','password_mismatch':'Passwords Do not Match!!'})
    latitude = forms.CharField(label='Latitude', widget=forms.TextInput(attrs={'class':'form-control'}))
    longitude = forms.CharField(label='Longitude', widget=forms.TextInput(attrs={'class':'form-control'}))
    location = forms.CharField(label='Location', widget=forms.TextInput(attrs={'class':'form-control'}))
    office_name = forms.CharField(label='Office Address', widget=forms.TextInput(attrs={'class':'form-control'}), error_messages={'required': 'Office Address required'},required=True)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2','latitude','longitude','location','office_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.save()
        return user

