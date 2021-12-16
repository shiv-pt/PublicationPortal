
from django.db import models
from django.db.models.fields import DateTimeCheckMixin
from django.http.request import split_domain_port

from upload_publication.models import Papers



# Create your models here.



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

# Pub_Detail=Pub_Details(SCOPUS_ID='FSD',PUBLON_ID='FSD',H_INDEX=0,I_INDEX=0,ORCHID='GD',publisher=Publisher.objects.get(pk=123))

class Issue(models.Model):
    ISSUEP_ID = models.AutoField(primary_key=True)
    CATEGORY = models.CharField(max_length=20)
    DESC = models.CharField(max_length=150)
    RESPONSE = models.CharField(max_length=60)
    ISSUE_STATUS = models.CharField(max_length=20)
    TIME_S= models.DateTimeField()
    PUB_ID = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ISSUE'

class Area_of_interest(models.Model):
    id=models.AutoField(primary_key=True)
    SAP_ID = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    INTEREST=models.CharField(max_length=70)

    class Meta:
        db_table = 'AREA_OF_INTEREST'
