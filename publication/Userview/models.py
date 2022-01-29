from django.contrib.auth.models import User
from django.db import models

from django.http.request import split_domain_port

from upload_publication.models import Papers
from django.utils.timezone import now


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Publisher(models.Model):
    SAP_ID = models.CharField(max_length=100, primary_key=True)
    DEPARTMENT = models.CharField(max_length=100)
    FIRST_NAME = models.CharField(max_length=100)
    MIDDLE_NAME = models.CharField(max_length=100,blank=True,default=None)
    LAST_NAME = models.CharField(max_length=100)
    PHONE_NUMBER = models.CharField(max_length=10)
    ROLE = models.CharField(max_length=100)
    DATE_OF_JOINING = models.DateField()
    EMAIL = models.EmailField()
    paper = models.ManyToManyField(Papers)

    class Meta:
        db_table = 'PUBLISHER'



class Pub_Details(models.Model):
    PUBD_ID = models.AutoField(primary_key=True)
    SCOPUS_ID = models.CharField(max_length=20)
    PUBLON_ID = models.CharField(max_length=20)
    H_INDEX = models.IntegerField()
    I_INDEX = models.IntegerField()
    ORCHID = models.CharField(max_length=20)
    publisher = models.OneToOneField(Publisher, on_delete=models.CASCADE)
    class Meta:
        db_table = 'PUB_DETAILS'


class Issue(models.Model):
    ISSUEP_ID = models.AutoField(primary_key=True)
    CATEGORY = models.CharField(max_length=20)
    DESC = models.CharField(max_length=250)
    ISSUE_STATUS = models.CharField(max_length=20,blank=True)
    TIME_S = models.DateTimeField(default=now, blank=True,null=True)
    PUB_ID = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ISSUE'

class Area_of_interest(models.Model):
    id=models.AutoField(primary_key=True)
    SAP_ID = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    INTEREST=models.CharField(max_length=70)

    class Meta:
        db_table = 'AREA_OF_INTEREST'
