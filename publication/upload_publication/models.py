from django.db import models


class Papers(models.Model):
    paper_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    doi = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='papers/pdfs/',blank=True)
    class Meta:
        db_table = 'paper'



class Reference(models.Model):
    ISSN = models.CharField(max_length=12, primary_key=True)
    ISSUE = models.CharField(max_length=50,blank=True, null=True)
    MONTH = models.CharField(max_length=10)
    PUB_YEAR = models.IntegerField()
    PGNO = models.IntegerField(blank=True, null=True)
    VOL = models.IntegerField(blank=True, null=True)
    LVL = models.CharField(max_length=15)
    ISSN_TYPE = models.CharField(max_length=10)
    PUB_TYPE = models.CharField(max_length=15)
    SCOPUS_INDEX= models.CharField(max_length=50,blank=True, null=True,default='N/A')
    WEB_OF_SCIENCE = models.CharField(max_length=50,blank=True, null=True,default='N/A')
    NAME = models.CharField(max_length=50)
    paper=models.OneToOneField(Papers,on_delete=models.CASCADE,default=None)

    class Meta:
        db_table = 'REFERENCE'

class Authors(models.Model):
    PAPER_ID = models.ForeignKey(Papers, on_delete=models.CASCADE)
    F_NAME=models.CharField(max_length=15)
    M_NAME=models.CharField(max_length=15,blank=True)
    L_NAME=models.CharField(max_length=15,blank=True)

    class Meta:
        db_table = 'AUTHORS'