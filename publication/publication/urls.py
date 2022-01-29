"""publication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import Pattern
from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static


from Userview.models import Issue
from . import views;
from upload_publication import views as upload_views
from register_login import views as register_views
from Adminview import views as admin_views
from Userview import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.showpdf),
    path('admin/',admin.site.urls),
    path('upload_publication/', upload_views.upload, name='upload_publication'),
    path('showpdf/', views.showpdf, name='showpdf'),
    path('login/', register_views.userLogin, name="login"),
    path('register/', register_views.userRegister, name="register"),
    path('logout/', register_views.userLogout, name="logout"),
    path('adminfeatures/', views.adminfeatures, name="adminfeatures"),
    path('userfeatures/', views.userfeatures, name="userfeatures"),
    path('publisher_details/', register_views.publisher_details, name="publisher_details"),
    path('paperdetails/<int:paperid>', views.paperdetails, name="paperdetails"),
    path('PapersReport/', admin_views.papersreport, name="PapersReport"),
    path('paper_references/', upload_views.paper_references,name="paper_references"),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='register_login/reset_password.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='register_login/password_reset_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='register_login/password_reset_confirm.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='register_login/password_reset_complete.html'), name="password_reset_complete"),

    path('chartView/',admin_views.chartView.as_view(), name="chartView"),
    path('yourPub/',user_views.yourPub, name="yourPub"),
    path('profile/',user_views.profile, name="profile"),
    path('issue/', user_views.issue, name="issue"),
    path('issuestatus/',user_views.issuestatus, name="issuestatus"),
    path('issue_delete/<int:id>/', user_views.issue_delete, name="issue_delete"),
    path('addressissues/', admin_views.address_issues, name="addressissues"),
    path('issue_status/<int:id>/<str:act>/', admin_views.issue_status, name="issue_status"),
    path('customReport/',admin_views.customReport, name="customReport"),
    path('customPDF/',admin_views.customPDF, name="customPDF"),
    path('customPub/',admin_views.customPub, name="customPub"),
    path('download_pdf/<int:paperid>', views.download_pdf, name='download_pdf'),
    path('edit_profile/', user_views.edit_profile, name="edit_profile"),
    path('publication/<int:year1>/<int:year2>/', views.sendpaper, name="sendpaper"),
    path('publication/<int:ident>/', views.senddetails, name="senddetails"),
    path('verify/<auth_token>', register_views.verify, name="verify"),
    path('error/', register_views.error_page, name="error"),
    path('token/', register_views.token_send, name="token_send"),
    path('accounts/login/' , register_views.userLogin , name="login_attempt"),
    path('searching/', views.searching, name="searching"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
