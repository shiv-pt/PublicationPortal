from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
# from .models import Profile

from django.conf import settings
from django.core.mail import send_mail
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
import time
from Userview.models import Publisher

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
                return render(request,'register_login/publisher_details.html')

        except Exception as e:
            print(e)
    page = 'register'
    return render(request, 'register_login/login_register.html', {'page': page})


def publisher_details(request):
    if request.method == 'POST':
        sap_id = request.POST['sap_id']
        department = request.POST['department']
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        role = request.POST['role']
        date_of_joining = request.POST['date_of_joining']
        email = request.POST['email']
        # print(sap_id)
        # print(department)
        # print(first_name)
        # print(middle_name)
        # print(last_name)
        # print(phone_number)
        # print(role)
        # print(date_of_joining)
        # print(email)

        try:
            pub=Publisher(SAP_ID=sap_id,DEPARTMENT=department,FIRST_NAME=first_name,MIDDLE_NAME=middle_name,LAST_NAME=last_name,PHONE_NUMBER=phone_number,ROLE=role,DATE_OF_JOINING=date_of_joining,EMAIL=email)
            print(pub)
            pub.save() 
            return redirect('/login/')
        except Exception as e:
            print(e)
            return redirect('/')

