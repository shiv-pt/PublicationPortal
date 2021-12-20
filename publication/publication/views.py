from django.shortcuts import render,redirect
from django.http import HttpResponse
from upload_publication.models import Papers
from django.core.files.storage import FileSystemStorage
from datetime import date

def showpdf(request):
    pdfs = Papers.objects.all()
    print(type(pdfs))
    return render(request, 'showpdf.html', {'pdfs': pdfs})

def userfeatures(request):
    if request.user.is_authenticated == False:
        return redirect('/login/')
    return render(request, 'userfeatures.html')


def adminfeatures(request):
    if request.user.is_authenticated == False:
        return redirect('/login/')
    return render(request, 'adminfeatures.html')


def paperdetails(request, paperid):
    papers = Papers.objects.raw('SELECT * FROM PAPER P, REFERENCE R, authors A WHERE A.PAPER_ID_id = p.paper_id AND P.paper_id = R.paper_id AND P.paper_id=%s',[paperid])
    if(len(papers)!=0):
        papers=papers[0]
        todays_date = date.today()
        #papers.MONTH = todays_date.year-papers.MONTH.month
    return render(request, 'paperdetails.html', {'paper': papers})


