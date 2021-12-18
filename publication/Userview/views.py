from django.shortcuts import render
from upload_publication.models import Papers
from Userview.models import Publisher
from datetime import date


# Create your views here.
def yourPub(request):
    userid = request.user.username
    print(userid)
    pdfs = Papers.objects.raw("SELECT * FROM PUBLISHER P, PUBLISHER_PAPER Q, PAPER R WHERE P.SAP_ID = Q.PUBLISHER_ID AND Q.PAPERS_ID = R.PAPER_ID AND P.SAP_ID = %s",[userid])
    return render(request, 'showpdf.html', {'pdfs': pdfs})

def profile(request):
    userid = request.user.username
    details = Publisher.objects.raw("SELECT * FROM PUBLISHER P, PUB_DETAILS Q WHERE P.SAP_ID = Q.PUBLISHER_ID AND P.SAP_ID= %s",[userid])
    if(len(details)!=0):
        details=details[0]
        todays_date = date.today()
        details.DATE_OF_JOINING=details.DATE_OF_JOINING.year-todays_date.year
    return render(request, 'profile.html', {'details': details})
