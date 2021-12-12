from django.shortcuts import render
from django.http import HttpResponse
from upload_publication.models import Papers
from django.core.files.storage import FileSystemStorage


def showpdf(request):
    pdfs = Papers.objects.all()
    return render(request, 'showpdf.html', {'pdfs': pdfs})

def userfeatures(request):
    return render(request, 'userfeatures.html')


def adminfeatures(request):
    return render(request, 'adminfeatures.html')

def paperdetails(request, paperid):
    paper = Papers.objects.get(title = paperid)
    return render(request, 'paperdetails.html',{'paper':paper})

