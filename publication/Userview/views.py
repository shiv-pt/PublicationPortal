from django.shortcuts import render
from upload_publication.models import Papers
from Userview.models import Publisher

# Create your views here.
def yourPub(request):
    userid = request.user.first_name
    pdfs = Papers.objects.raw("SELECT * FROM PUBLISHER P, PUBLISHER_PAPER Q, PAPER R WHERE P.SAP_ID = Q.PUBLISHER_ID AND Q.PAPERS_ID = R.PAPER_ID AND P.FIRST_NAME = %s",[userid])
    print(pdfs)
    return render(request, 'showpdf.html', {'pdfs': pdfs})

def profile(request):
    userid = request.user.last_name
    print(userid)
    details = Publisher.objects.raw("SELECT * FROM PUBLISHER P, PUB_DETAILS Q WHERE P.SAP_ID = Q.PUBLISHER_ID AND P.LAST_NAME= %s",[userid])
    print(details)
    return render(request, 'profile.html', {'details': details})