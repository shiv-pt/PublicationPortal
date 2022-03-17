from django.shortcuts import redirect, render
from django.utils.timezone import now
from Userview.models import Issue
from Userview.models import Pub_Details
from upload_publication.models import Papers
from Userview.models import Publisher
from datetime import date
from django.contrib.auth.models import User
from django.core.paginator import Paginator



# Create your views here.
def yourPub(request):
    userid = request.user.username
    print(userid)
    pdfs = Papers.objects.raw("SELECT * FROM PUBLISHER P, PUBLISHER_PAPER Q, PAPER R,REFERENCE S WHERE P.SAP_ID = Q.PUBLISHER_ID AND Q.PAPERS_ID = R.PAPER_ID AND R.paper_id=S.paper_id AND P.SAP_ID = %s",[userid])
    paginator = Paginator(pdfs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'showpdf.html', {'pdfs': page_obj,'type':'yourPub'})

def profile(request):
    userid = request.user.username
    details = Publisher.objects.raw("SELECT * FROM PUBLISHER P, PUB_DETAILS Q WHERE P.SAP_ID = Q.PUBLISHER_ID AND P.SAP_ID= %s",[userid])
    print(details)
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
        issue=Issue(CATEGORY=CATEGORY,DESC=DESC,ISSUE_STATUS='Pending',PUB_ID=pub)
        issue.save()
        return redirect("/issuestatus")
    
    return render(request, 'issue.html')

def issuestatus(request):
    userid=request.user.username
    issues=Issue.objects.raw("SELECT * FROM ISSUE I, PUBLISHER P WHERE I.PUB_ID_id = P.SAP_ID AND P.SAP_ID = %s",[userid])
    paginator = Paginator(issues, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'issuestatus.html', {'issues': page_obj})

def issue_delete(request,id):
    print(id)
    issue=Issue.objects.get(ISSUEP_ID=id)
    issue.delete()
    return redirect("/addressissues")

def edit_profile(request):
    userid=request.user.username
    details=Publisher.objects.raw("SELECT * FROM PUBLISHER P, PUB_DETAILS Q WHERE P.SAP_ID = Q.PUBLISHER_ID AND P.SAP_ID= %s",[userid])
    details = details[0]
    details.FIRST_NAME = details.FIRST_NAME.split('. ', 1)[1]
    if request.method=='POST':
        email=request.POST.get('email')
        if User.objects.filter(email=email).first() is not None and email!=request.user.email:
            msg = {'msg': 'Email already exists'}
            print(msg)
            return render(request, 'edit_profile.html', {'details': details,'msg':msg})
        pub=Publisher.objects.get(SAP_ID=userid)
        title = request.POST.get('title')
        first_name = title+". "+request.POST.get('first_name')
        pub.FIRST_NAME=first_name
        pub.MIDDLE_NAME=request.POST.get('middle_name')
        pub.LAST_NAME=request.POST.get('last_name')
        pub.EMAIL=email
        pub.DATE_OF_JOINING=request.POST.get('date_of_joining')
        pub.PHONE_NUMBER=request.POST.get('phone_number')
        pub.DEPARTMENT=request.POST.get('department')
        pub.ROLE=request.POST.get('role')
        pub.save()
        pub_details=Pub_Details.objects.get(publisher=userid)
        pub_details.SCOPUS_ID=request.POST.get('scopus_id')
        pub_details.PUBLON_ID=request.POST.get('publon_id')
        pub_details.H_INDEX = request.POST.get('h_index')
        pub_details.I_INDEX = request.POST.get('i_index')
        pub_details.ORCHID = request.POST.get('orchid_id')
        pub_details.save()

        user_ob=User.objects.get(username=userid)
        user_ob.first_name=first_name
        user_ob.last_name=request.POST.get('last_name')
        user_ob.email=email
        user_ob.save()
        return redirect("/profile")
    return render(request, 'edit_profile.html',{"details":details})
