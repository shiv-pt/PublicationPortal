from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
import uuid
from django.conf import settings
from django.core.mail import send_mail
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
import time

# Create your views here.


def userLogout(request):
    logout(request)
    return redirect('/')


def userLogin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        user_ob = User.objects.filter(username=username).first()
        print(user_ob)
       
        if user_ob is None:
         
            messages.add_message(request, messages.INFO, 'User not found')
            return redirect('login')

        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
           
            messages.add_message(request, messages.INFO,
                                 'Wrong creds')
            return redirect('login')
       
        login(request, user)
        return redirect('/')
    page = 'login'
    return render(request, 'register_login/login_register.html', {'page': page})


def userRegister(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            if User.objects.filter(email=email).first() is not None:
                print(User.objects.filter(email=email).first())
                messages.add_message(
                    request, messages.INFO, 'email name taken')
                render(request, 'register_login/login_register.html')

            elif User.objects.filter(username=username).first() is not None:
                messages.add_message(request, messages.INFO, 'User name taken')
                render(request, 'register_login/login_register.html')

            else:
                user_ob = User.objects.create(username=username, email=email)
                user_ob.set_password(password)
                user_ob.save()

            profile_ob = Profile.objects.create(
                user=user_ob)
            profile_ob.save()
        except Exception as e:
            print(e)
    page = 'register'
    return render(request, 'register_login/login_register.html', {'page': page})


