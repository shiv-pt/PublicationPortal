from asyncio.windows_events import NULL
import bs4
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
# from .models import Profile
import uuid

from django.conf import settings
from django.core.mail import send_mail
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
import time

import requests
from Userview.models import Publisher
from Userview.models import Profile
from Userview.models import Pub_Details
from Userview.models import Area_of_interest

# Create your views here.




def userLogout(request):
    logout(request)
    return redirect('/')


def userLogin(request):
    page = 'login'
    print(page)
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        user_ob = User.objects.filter(username=username).first()
        print(user_ob)
       
        if user_ob is None:
            msg={'msg':'User does not exist'}
            print(msg)
            return render(request, 'register_login/login_register.html', {"page": page,"msg": msg})
        if username=='Admin':
            user = authenticate(username=username, password=password)
            print(user)
            if user is None:
                msg = {'msg': 'Invalid Credentials'}
                print(msg)
                return render(request, 'register_login/login_register.html', {'page': page, 'msg': msg})

            login(request, user)
            return redirect('/')
        profile_obj = Profile.objects.filter(user = user_ob).first()
        if not profile_obj.is_verified:
            msg={'msg':'Profile not verified, check your mail'}
            return render(request, 'register_login/login_register.html', {"page": page,"msg": msg})
        
        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            msg={'msg':'Invalid Credentials'}
            print(msg)
            return render(request, 'register_login/login_register.html', {'page': page,'msg': msg})
       
        login(request, user)
        return redirect('/')
    return render(request, 'register_login/login_register.html', {'page': page})

def webscrapPubDetails(first_name,last_name):
    linkbeg = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C33&q="
    name = first_name + " " + last_name
    name = name+" rvce"+"&btnG="
    name = name.replace(' ', '+')

    link = linkbeg+name

    res = requests.get(link)
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    info = soup.find_all("h4", attrs={"class": "gs_rt2"})

    ref = []
    name = []
    h_index=''
    i_index=''

    for i in info:
        if i.find('a'):
            ref.append(i.find('a')['href'])
            name.append(i.find('a').text)

    if len(ref) != 0:
        profilelink = "https://scholar.google.com"+ref[0]
        profileaccess = requests.get(profilelink)
        beautisoup = bs4.BeautifulSoup(profileaccess.text, "lxml")

        citinfo = beautisoup.find_all("td", attrs={"class": "gsc_rsb_std"})
        h_index = citinfo[2].text
        i_index = citinfo[4].text

    # linkforpub = "https://www.google.com/search?q="+first_name+"+"+last_name+"+rvce+irins+profile"
    # print(linkforpub)
    # res2=requests.get(linkforpub)
    # soup2=bs4.BeautifulSoup(res2.text,'lxml')
    # # print(soup2)
    # info2 = soup2.find_all("div", attrs={"class": "kCrYT"})
    # print(info2)
    return h_index,i_index

def userRegister(request):
    page = 'register'
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if User.objects.filter(email=email).first() is not None:
            msg={'msg':'Email already exists'}
            print(msg)
            return render(request, 'register_login/login_register.html', {'msg': msg,'page': page})
        elif User.objects.filter(username=username).first() is not None:
            msg={'msg':'Username already exists'}
            print(msg)
            return render(request, 'register_login/login_register.html', {'msg': msg,'page': page})

        # CODE FOR WEB SCRAPPING

        h_index,i_index=webscrapPubDetails(first_name,last_name)


        # CODE FOR WEB SCRAPPING ENDS
        cred={'username':username,'email':email,'password':password,'first_name':first_name,'last_name':last_name,'h_index':h_index,'i_index':i_index}
        return render(request, 'register_login/publisher_details.html',{'cred':cred})
    return render(request, 'register_login/login_register.html', {'page': page})


def publisher_details(request):
    if request.method == 'POST':
        sap_id = request.POST['sap_id']
        department = request.POST['department']
        title=request.POST['title']
        first_name = request.POST['first_name']
        first_name=title+". "+first_name
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        role = request.POST['role']
        date_of_joining = request.POST['date_of_joining']
        email = request.POST['email']
        scopus_id = request.POST['scopus_id']
        if scopus_id=='':
            scopus_id=NULL
        publon_id = request.POST['publon_id']
        if publon_id=='':
            publon_id=NULL
        h_index = request.POST['h_index']
        if h_index=='':
            h_index=NULL
        i_index = request.POST['i_index']
        if i_index=='':
            i_index=NULL
        orchid_id = request.POST['orchid_id']
        if orchid_id=='':
            orchid_id=NULL
        password = request.POST['password']
        username=sap_id
        
        s='aoi0'
        prev=''
        num=0

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
                user_ob = User.objects.create(username=username, email=email,first_name=first_name,last_name=last_name)
                user_ob.set_password(password)
                user_ob.save()
                
            try:
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(user = user_ob , auth_token = auth_token)
                profile_obj.save()
                send_mail_after_registration(email , auth_token)
                pub = Publisher(SAP_ID=sap_id, DEPARTMENT=department, FIRST_NAME=first_name, MIDDLE_NAME=middle_name,
                                LAST_NAME=last_name, PHONE_NUMBER=phone_number, ROLE=role, DATE_OF_JOINING=date_of_joining, EMAIL=email)
                print(pub)
                pub.save()
                pub_det = Pub_Details(SCOPUS_ID=scopus_id, PUBLON_ID=publon_id,
                                    H_INDEX=h_index, I_INDEX=i_index, ORCHID=orchid_id, publisher=pub)
                print(pub_det)
                pub_det.save()
                while request.POST[s] != '':
                    num += 1
                    prev=s
                    s = 'aoi'+str(num)
                    try:
                        if request.POST[s] != '':
                            aoi_ob = Area_of_interest(SAP_ID=pub,INTEREST=request.POST[prev])
                            aoi_ob.save()
                            print(aoi_ob)
                    except:
                        break
                try:
                    aoi_ob = Area_of_interest(SAP_ID=pub, INTEREST=request.POST[prev])
                    aoi_ob.save()

                except:
                    pass
                #login(request, user_ob)
                return redirect('/token')
            except Exception as e:
                print(e)
                return redirect('/')
        except Exception as e:
            print(e)

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'error.html')


def token_send(request):
    return render(request , 'token.html')
