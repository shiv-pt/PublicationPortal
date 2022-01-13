from django.shortcuts import render,redirect
from django.http import HttpResponse
from upload_publication.models import Papers
from django.core.files.storage import FileSystemStorage
from datetime import date
import os
from wsgiref.util import FileWrapper
import urllib
import mimetypes

def showpdf(request):
    pdfs = Papers.objects.raw('SELECT * FROM PAPER P, REFERENCE R WHERE P.paper_id = R.paper_id')
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
    papers = Papers.objects.raw('SELECT * FROM PAPER P, REFERENCE R, authors A WHERE A.PAPER_ID_id = P.paper_id AND P.paper_id = R.paper_id AND P.paper_id=%s',[paperid])
    print(len(papers))
    author=''
    for i in range(0,len(papers)-1):
        author = author + papers[i].A_NAME + ', '
    if(len(papers)>0):
        author = author + papers[len(papers)-1].A_NAME
    if(len(papers)!=0):
        papers=papers[0]
    papers.A_NAME = author
    return render(request, 'paperdetails.html', {'paper': papers})


def download_pdf(request, paperid):
    paper=Papers.objects.get(paper_id=paperid)
    fs = FileSystemStorage()
    filename = paper.pdf
    filename=str(filename)
    name=filename[12:]
    filepath = os.path.join(fs.location, filename)
    wrapper = FileWrapper(open(filepath, 'rb'))
    content_type = mimetypes.guess_type(filepath)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = "attachment; filename=%s" % name
    return response
