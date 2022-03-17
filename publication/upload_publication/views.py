from django.shortcuts import redirect, render
from django.http import HttpResponse
from Userview.models import Publisher
from upload_publication.models import Authors
from upload_publication.models import Reference
from upload_publication.models import Papers
from django.core.files.storage import FileSystemStorage


def paperwebscrap(title):
    a=title

def upload(request):
    if request.user.is_authenticated==False:
        return redirect('/login/')
    if request.method=='POST':

        paperwebscrap(request.POST.get('title'))
        paper = {'title': request.POST.get('title'), 'doi': request.POST.get('doi')}
        return render(request, 'upload_publication/paper_references.html', {'paper': paper})
    return render(request, 'upload_publication/upload.html')
    

def paper_references(request):
    if request.method=='POST':
        userid=request.user.username
        savepaper=Papers()
        savepaper.title = request.POST.get('title')
        doi= request.POST.get('doi')
        if doi=='':
            savepaper.doi=None
        else:
            savepaper.doi=doi  
        try: 
            pdf = request.FILES['pdf']
            savepaper.pdf = pdf
        except:
            savepaper.pdf=None
        savepaper.save()
        ISSN=request.POST.get('ISSN')
        ISSUE=request.POST.get('ISSUE')
        if ISSUE=='':
            ISSUE=None
        MONTH=request.POST.get('MONTH')
        PUB_YEAR=request.POST.get('PUB_YEAR')
        PGNO=request.POST.get('PGNO')
        if PGNO=='':
            PGNO=None
        VOL=request.POST.get('VOL')
        if VOL=='':
            VOL=None
        LVL=request.POST.get('LVL')
        ISSN_TYPE=request.POST.get('ISSN_TYPE')
        PUB_TYPE=request.POST.get('PUB_TYPE')
        SCOPUS_INDEX=request.POST.get('SCOPUS_INDEX')
        if(SCOPUS_INDEX==''):
            SCOPUS_INDEX=None
        WEB_OF_SCIENCE=request.POST.get('WEB_OF_SCIENCE')
        if(WEB_OF_SCIENCE==''):
            WEB_OF_SCIENCE=None
        RANKING=request.POST.get('RANKING')
        if(RANKING==''):
            RANKING=None
        NAME=request.POST.get('NAME')
        pap_refer=Reference(ISSN=ISSN,ISSUE=ISSUE,MONTH=MONTH,PUB_YEAR=PUB_YEAR,PGNO=PGNO,VOL=VOL,LVL=LVL,ISSN_TYPE=ISSN_TYPE,PUB_TYPE=PUB_TYPE,SCOPUS_INDEX=SCOPUS_INDEX,WEB_OF_SCIENCE=WEB_OF_SCIENCE,RANKING=RANKING,NAME=NAME,paper=savepaper)
        pap_refer.save()
        
        pub=Publisher.objects.get(pk=userid)
        pub.paper.add(savepaper)
        
        s = 'author0'
        prev = ''
        num = 0

        while request.POST[s] != '':
            num += 1
            prev = s
            s = 'author'+str(num)
            try:
                if request.POST[s] != '':
                    author_ob = Authors(PAPER_ID=savepaper,A_NAME=request.POST[prev])
                    author_ob.save()
            except:
                break
        author_ob = Authors(PAPER_ID=savepaper,A_NAME=request.POST[prev])
        author_ob.save()


        return redirect('/')
    return render(request, 'upload_publication/paper_references.html')

