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
from . import views;
from upload_publication import views as upload_views
from register_login import views as register_views
from Adminview import views as admin_views
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
    path('paperdetails/(?P<paperid>[-a-zA-Z0-9_]+)$', views.paperdetails, name="paperdetails"),
    path('PapersReport/', admin_views.papersreport, name="PapersReport"),
    path('chart',admin_views.chartView.as_view(), name="chartView")
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
