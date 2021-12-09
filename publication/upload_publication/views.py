from django.shortcuts import redirect, render
from django.http import HttpResponse
from upload_publication.models import Papers
from django.core.files.storage import FileSystemStorage

def upload(request):
    
    if request.method=='POST':
        
        if request.POST.get('title') and request.POST.get('doi') and request.FILES['pdf']:
            
            savepaper=Papers()
            savepaper.title = request.POST.get('title')
            savepaper.doi = request.POST.get('doi')
            savepaper.pdf=request.FILES['pdf']
            savepaper.save()
            return redirect('/')
    return render(request, 'upload_publication/upload.html')
    