from django.shortcuts import redirect, render
from django.utils.timezone import now
from Userview.models import Issue
from upload_publication.models import Papers
from Userview.models import Publisher
from datetime import date



# Create your views here.
def yourPub(request):
    userid = request.user.username
    print(userid)
    pdfs = Papers.objects.raw("SELECT * FROM PUBLISHER P, PUBLISHER_PAPER Q, PAPER R WHERE P.SAP_ID = Q.PUBLISHER_ID AND Q.PAPERS_ID = R.PAPER_ID AND P.SAP_ID = %s",[userid])
    print(pdfs)
    return render(request, 'showpdf.html', {'pdfs': pdfs})

def profile(request):
    userid = request.user.username
    details = Publisher.objects.raw("SELECT * FROM PUBLISHER P, PUB_DETAILS Q WHERE P.SAP_ID = Q.PUBLISHER_ID AND P.SAP_ID= %s",[userid])
    if(len(details)!=0):
        details=details[0]
        todays_date = date.today()
        details.DATE_OF_JOINING = todays_date.year-details.DATE_OF_JOINING.year
    return render(request, 'profile.html', {'details': details})

def issue(request):
    if request.method=='POST':
        userid=request.user.username
        CATEGORY=request.POST.get('CATEGORY')
        DESC=request.POST.get('DESC')
        pub=Publisher.objects.get(SAP_ID=userid)
        print(pub)
        issue=Issue(CATEGORY=CATEGORY,DESC=DESC,RESPONSE='Pending',ISSUE_STATUS='Pending',PUB_ID=pub)
        issue.save()
        return redirect("/issuestatus")
    
    return render(request, 'issue.html')

def issuestatus(request):
    userid=request.user.username
    issues=Issue.objects.raw("SELECT * FROM ISSUE I, PUBLISHER P WHERE I.PUB_ID_id = P.SAP_ID AND P.SAP_ID = %s",[userid])
    return render(request, 'issuestatus.html', {'issues': issues})

def issue_delete(request,id):
    print(id)
    issue=Issue.objects.get(ISSUEP_ID=id)
    issue.delete()
    if(request.user.username=="admin"):
        return redirect("/addressissues")
    else:
        return redirect("/issuestatus")
