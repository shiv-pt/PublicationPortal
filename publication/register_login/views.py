import bs4
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

import requests
from Userview.models import Publisher
from Userview.models import Pub_Details
from Userview.models import Area_of_interest

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
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        h_index=''
        i_index=''
        # CODE FOR WEB SCRAPPING

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


        for i in info:
            if i.find('a'):
                ref.append(i.find('a')['href'])
                name.append(i.find('a').text)

        if len(ref) != 0:
            profilelink = "https://scholar.google.com"+ref[0]
            profileaccess = requests.get(profilelink)
            beautisoup = bs4.BeautifulSoup(profileaccess.text, "lxml")

            citinfo = beautisoup.find_all("td", attrs={"class": "gsc_rsb_std"})
            h_index= citinfo[2].text
            i_index= citinfo[4].text

        else:
            print("Data Not Found")

        # CODE FOR WEB SCRAPPING ENDS


        cred={'username':username,'email':email,'password':password,'first_name':first_name,'last_name':last_name,'h_index':h_index,'i_index':i_index}
        return render(request, 'register_login/publisher_details.html',{'cred':cred})
    page = 'register'
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
        publon_id = request.POST['publon_id']
        h_index = request.POST['h_index']
        i_index = request.POST['i_index']
        orchid_id = request.POST['orchid_id']
        password = request.POST['password']
        username=sap_id
        # print(sap_id)
        # print(department)
        # print(first_name)
        # print(middle_name)
        # print(last_name)
        # print(phone_number)
        # print(role)
        # print(date_of_joining)
        # print(email)
        # print(scopus_id)
        # print(publon_id)
        # print(h_index)
        # print(i_index)
        # print(orchid_id)
        # print(email)
        # print(username)
        # print(password)
        # print(request.POST)
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
                aoi_ob = Area_of_interest(SAP_ID=pub, INTEREST=request.POST[prev])
                aoi_ob.save()
                print(aoi_ob)
                return redirect('/login/')
            except Exception as e:
                print(e)
                return redirect('/')
        except Exception as e:
            print(e)


