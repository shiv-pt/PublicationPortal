from django.shortcuts import render,redirect
from django.http import HttpResponse
from upload_publication.models import Papers
from django.core.files.storage import FileSystemStorage
from datetime import date
import os
from wsgiref.util import FileWrapper
import urllib
import mimetypes
from django.http import JsonResponse
from django.core.paginator import Paginator

def showpdf(request):
    pdfs = Papers.objects.raw('SELECT * FROM PAPER P, REFERENCE R WHERE P.paper_id = R.paper_id')
    paginator = Paginator(pdfs, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'showpdf.html', {'pdfs': page_obj})

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
    try:
        wrapper = FileWrapper(open(filepath, 'rb'))
        content_type = mimetypes.guess_type(filepath)[0]
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Length'] = os.path.getsize(filepath)
        response['Content-Disposition'] = "attachment; filename=%s" % name
        return response
    except:
        return HttpResponse("File not found")

def senddetails(request,ident):
    papers=Papers.objects.raw('SELECT * FROM PAPER P, REFERENCE R, authors A WHERE A.PAPER_ID_id = P.paper_id AND P.paper_id = R.paper_id AND P.paper_id = %s',[ident])
    print(papers,"Hello",len(papers))
    data=[]
    i=0
    while i<len(papers):
        print(i)
        id=papers[i].paper_id
        ind=id
        authors=[]
        authors.append(papers[i].A_NAME)
        i=i+1
        while i<len(papers) and id==papers[i].paper_id:
            authors.append(papers[i].A_NAME)
            id = papers[i].paper_id
            i=i+1
        print(i)
        print()
        datajson={'ID':papers[i-1].paper_id,'Title':papers[i-1].title,'Year':papers[i-1].PUB_YEAR,'Month':papers[i-1].MONTH,'Level':papers[i-1].LVL,'Volume':papers[i-1].VOL,'Pages':papers[i-1].PGNO,'DOI':papers[i-1].doi,'Issue':papers[i-1].ISSUE,'ISSN':papers[i-1].ISSN,'ISSN_TYPE':papers[i-1].ISSN_TYPE,'Publication Type':papers[i-1].PUB_TYPE,'Scopus Index':papers[i-1].SCOPUS_INDEX,'Web of Science':papers[i-1].WEB_OF_SCIENCE,'Ranking':papers[i-1].RANKING,'Authors':authors}
        print(datajson)
        data.append(datajson) 

    return JsonResponse(data,safe=False)

def sendpaper(request,year1,year2):
    papers=Papers.objects.raw('SELECT * FROM PAPER P, REFERENCE R, authors A WHERE A.PAPER_ID_id = P.paper_id AND P.paper_id = R.paper_id AND R.PUB_YEAR BETWEEN %s AND %s',[year1,year2])
    print(papers)
    data=[]
    i=0
    while i<len(papers):
        print(i)
        id=papers[i].paper_id
        ind=id
        authors=[]
        authors.append(papers[i].A_NAME)
        i=i+1
        while i<len(papers) and id==papers[i].paper_id:
            authors.append(papers[i].A_NAME)
            id = papers[i].paper_id
            i=i+1
        print(i)
        print()
        datajson={'ID':papers[i-1].paper_id,'Title':papers[i-1].title,'Year':papers[i-1].PUB_YEAR,'Month':papers[i-1].MONTH,'Level':papers[i-1].LVL,'Volume':papers[i-1].VOL,'Pages':papers[i-1].PGNO,'DOI':papers[i-1].doi,'Issue':papers[i-1].ISSUE,'ISSN':papers[i-1].ISSN,'ISSN_TYPE':papers[i-1].ISSN_TYPE,'Publication Type':papers[i-1].PUB_TYPE,'Scopus Index':papers[i-1].SCOPUS_INDEX,'Web of Science':papers[i-1].WEB_OF_SCIENCE,'Ranking':papers[i-1].RANKING,'Authors':authors}
        print(datajson)
        data.append(datajson) 

    return JsonResponse(data,safe=False)


def searchdata(searchtext):
    searchwords = searchtext.split()
    if len(searchwords) > 0:
        pdfdict = {}
        for word in searchwords:
            pdfs = Papers.objects.filter(title__icontains=word)
            for i in pdfs:
                if i in pdfdict.keys():
                    pdfdict[i] += 1
                else:
                    pdfdict[i] = 1
            print(pdfdict)
        matdict = sorted(pdfdict.items(), key=lambda x: x[1], reverse=True)
        pdflist = []
        for i in matdict:
            pdflist.append(i[0])
    return pdflist

def searching(request):

    allpdfs = Papers.objects.raw(
        'SELECT * FROM PAPER P, REFERENCE R WHERE P.paper_id = R.paper_id')
    
    if request.method == 'POST':
        searchtext = request.POST['searchtext']
        pdfsreturned = searchdata(searchtext)
        pdfs = []
        for i in allpdfs:
            for j in pdfsreturned:
                if i.paper_id == j.paper_id:
                    pdfs.append(i)
        print(pdfs)
        paginator = Paginator(pdfs, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'showpdf.html', {'pdfs': page_obj})
    
    paginator = Paginator(allpdfs, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'showpdf.html', {'pdfs': page_obj})
