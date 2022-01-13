from datetime import date
from django.shortcuts import redirect, render
from upload_publication.models import Papers, Reference
from Userview.models import Publisher
from Userview.models import Issue
from django.views.generic import TemplateView
from Userview.models import Issue
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from django.db import connection
from django.core import serializers
# Create your views here.

def customPub(request):
    if(request.method=="POST"):
        input = request.POST.get('publisher')
        id = input[0:11]
        print(id)
        data = Papers.objects.raw(
            'SELECT * FROM PUBLISHER P, publisher_paper Q, PAPER R, REFERENCE S WHERE P.SAP_ID=Q.publisher_id AND Q.papers_id=R.paper_id AND R.paper_id=S.paper_id AND P.SAP_ID=%s',[id])
        data1 = Reference.objects.raw('SELECT * FROM PUBLISHER P, publisher_paper Q, PAPER R, REFERENCE S WHERE P.SAP_ID=Q.publisher_id AND Q.papers_id=R.paper_id AND R.paper_id=S.paper_id AND P.SAP_ID=%s',[id])
        pub = Publisher.objects.all()
        name={"name":input[13:]}
        request.session['mycache'] = serializers.serialize('json', data)
        request.session['mycache1'] = serializers.serialize('json', data1)
        return render(request, 'custompub.html', {"pub": pub, "data": data,"name":name})
    pub = Publisher.objects.all()
    data = Papers.objects.raw('SELECT * FROM paper P, reference R WHERE P.PAPER_ID = R.PAPER_ID ORDER BY R.PUB_YEAR')
    data1 = Reference.objects.raw('SELECT * FROM paper P, reference R WHERE P.PAPER_ID = R.PAPER_ID ORDER BY R.PUB_YEAR')
    request.session['mycache'] = serializers.serialize('json', data)
    request.session['mycache1'] = serializers.serialize('json', data1)
    return render(request, 'custompub.html', {"pub": pub, "data": data})


def customPDF(request):
    print(request.session.get('mycache'))
    data = list(serializers.deserialize("json",request.session.get('mycache')))
    data1 = list(serializers.deserialize("json",request.session.get('mycache1')))
    print(data)
    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter)
    c.setFont("Helvetica",25)
    c.setTitle("Custom Report")
    c.drawString(230,680,"Generated Report")
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",10)
    textob.textLine("All uploaded papers")
    lines = []
    c.drawImage("static/img/header.jpg",15,720, width = 650, height = 40)
    header = ['Title', 'DOI','Published in', 'Year','Month', 'Scopus', 'WOS']
    lines.append(header)
    for pdf in data:
        print("pdf", pdf.object.paper_id)
        line = []
        line.append(pdf.object.title)
        line.append(pdf.object.doi)
        for p in data1:
            print("p", p.object.paper_id)
            if(pdf.object.paper_id == p.object.paper_id):
                line.append(p.object.PUB_TYPE +" - \n "+ p.object.NAME)
                line.append(p.object.PUB_YEAR)
                line.append(p.object.MONTH)
                line.append(p.object.SCOPUS_INDEX)
                line.append(p.object.WEB_OF_SCIENCE)
        lines.append(line)
    f = Table(lines,colWidths=[150,40,150,35,55,50,50])
    f.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('FONTSIZE',(0,0),(-1,0),14),
                            ('BOTTOMPADDING',(0,0),(-1,0),12)]))
    f.wrapOn(c,10, 10)
    f.drawOn(c, 50, 480)
    # c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='CustomReport.pdf')

def customReport(request):
    if(request.method == 'POST'):
        startdate=request.POST['startyear']
        enddate=request.POST['endyear']
        scopus=request.POST.get('scopus')
        doi=request.POST.get('doi')
        wos=request.POST.get('wos')
        date={"startyear":startdate,"endyear":enddate}
        
        if scopus and doi and wos:
            data = Papers.objects.raw('SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NOT NULL AND R.SCOPUS_INDEX IS NOT NULL AND R.WEB_OF_SCIENCE IS NOT NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s',[startdate,enddate])
            data1 = Reference.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NOT NULL AND R.SCOPUS_INDEX IS NOT NULL AND R.WEB_OF_SCIENCE IS NOT NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s', [startdate, enddate])
            request.session['mycache'] = serializers.serialize('json', data)
            request.session['mycache1'] = serializers.serialize('json', data1)
            return render(request, 'customreport.html', {"data": data,"date":date})
        elif scopus and doi:
            data = Papers.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NOT NULL AND R.SCOPUS_INDEX IS NOT NULL AND R.WEB_OF_SCIENCE IS NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s', [startdate, enddate])
            data1 = Reference.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NOT NULL AND R.SCOPUS_INDEX IS NOT NULL AND R.WEB_OF_SCIENCE IS NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s', [startdate, enddate])
            request.session['mycache'] = serializers.serialize('json', data)
            request.session['mycache1'] = serializers.serialize('json', data1)
            return render(request, 'customreport.html', {"data": data, "date": date})
        elif scopus and wos:
            data = Papers.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NULL AND R.SCOPUS_INDEX IS NOT NULL AND R.WEB_OF_SCIENCE IS NOT NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s', [startdate, enddate])
            data1 = Reference.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NULL AND R.SCOPUS_INDEX IS NOT NULL AND R.WEB_OF_SCIENCE IS NOT NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s', [startdate, enddate])
            request.session['mycache'] = serializers.serialize('json', data)
            request.session['mycache1'] = serializers.serialize('json', data1)
            return render(request, 'customreport.html', {"data": data, "date": date})
        elif doi and wos:
            data = Papers.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NOT NULL AND R.SCOPUS_INDEX IS NULL AND R.WEB_OF_SCIENCE IS NOT NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s', [startdate, enddate])
            data1 = Reference.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NOT NULL AND R.SCOPUS_INDEX IS NULL AND R.WEB_OF_SCIENCE IS NOT NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s', [startdate, enddate])
            request.session['mycache'] = serializers.serialize('json', data)
            request.session['mycache1'] = serializers.serialize('json', data1)
            return render(request, 'customreport.html', {"data": data, "date": date})
        elif scopus:
            data = Papers.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NULL AND R.SCOPUS_INDEX IS NOT NULL AND R.WEB_OF_SCIENCE IS NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s', [startdate, enddate])
            data1 = Reference.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NULL AND R.SCOPUS_INDEX IS NOT NULL AND R.WEB_OF_SCIENCE IS NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s', [startdate, enddate])
            request.session['mycache'] = serializers.serialize('json', data)
            request.session['mycache1'] = serializers.serialize('json', data1)
            return render(request, 'customreport.html', {"data": data, "date": date})
        elif doi:
            data = Papers.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NOT NULL AND R.SCOPUS_INDEX IS NULL AND R.WEB_OF_SCIENCE IS NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s', [startdate, enddate])
            data1 = Reference.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NOT NULL AND R.SCOPUS_INDEX IS NULL AND R.WEB_OF_SCIENCE IS NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s', [startdate, enddate])
            request.session['mycache'] = serializers.serialize('json', data)
            request.session['mycache1'] = serializers.serialize('json', data1)
            return render(request, 'customreport.html', {"data": data, "date": date})
        elif wos:
            data = Papers.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NULL AND R.SCOPUS_INDEX IS NULL AND R.WEB_OF_SCIENCE IS NOT NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s', [startdate, enddate])
            data1 = Reference.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id = R.paper_id AND P.doi IS NULL AND R.SCOPUS_INDEX IS NULL AND R.WEB_OF_SCIENCE IS NOT NULL AND R.PUB_YEAR>=%s AND R.PUB_YEAR<=%s', [startdate, enddate])
            request.session['mycache'] = serializers.serialize('json', data)
            request.session['mycache1'] = serializers.serialize('json', data1)
            return render(request, 'customreport.html', {"data": data, "date": date})
        else:
            data = Papers.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id=R.paper_id AND P.doi IS NULL AND R.SCOPUS_INDEX IS NULL AND R.WEB_OF_SCIENCE IS NULL AND R.PUB_YEAR >= %s AND R.PUB_YEAR <= %s', [startdate, enddate])
            data1 = Reference.objects.raw(
                'SELECT * FROM paper P, reference R WHERE P.paper_id=R.paper_id AND P.doi IS NULL AND R.SCOPUS_INDEX IS NULL AND R.WEB_OF_SCIENCE IS NULL AND R.PUB_YEAR >= %s AND R.PUB_YEAR <= %s', [startdate, enddate])
            request.session['mycache'] = serializers.serialize('json', data)
            request.session['mycache1'] = serializers.serialize('json', data1)
    data = Papers.objects.raw('SELECT * FROM paper P, reference R WHERE P.PAPER_ID = R.PAPER_ID ORDER BY R.PUB_YEAR')
    data1 = Reference.objects.raw('SELECT * FROM paper P, reference R WHERE P.PAPER_ID = R.PAPER_ID ORDER BY R.PUB_YEAR')
    request.session['mycache'] = serializers.serialize('json', data)
    request.session['mycache1'] = serializers.serialize('json', data1)
    return render(request, 'customreport.html', {"data": data})


def issue_status(request,id,act):
    print(id,act)
    obj = Issue.objects.filter(ISSUEP_ID = id).update(ISSUE_STATUS=act)
    return redirect('/addressissues')
    
def address_issues(request):
    issues = Issue.objects.all()
    return render(request, 'address.html', {'issues': issues})

class chartView(TemplateView):
    template_name = "chart/charts.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = Papers.objects.raw('SELECT ISSN, paper_id, PUB_YEAR, COUNT(PUB_YEAR) CNT FROM REFERENCE GROUP BY PUB_YEAR')
        context["data"] = Papers.objects.raw('SELECT * FROM paper P, reference R WHERE P.PAPER_ID = R.PAPER_ID ORDER BY R.PUB_YEAR')
        context["is"] = Issue.objects.raw('SELECT ISSUEP_ID, ISSUE_STATUS, COUNT(ISSUE_STATUS) CNT FROM issue GROUP BY ISSUE_STATUS')
        return context

    

def papersreport(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter)
    c.setFont("Helvetica",25)
    c.setTitle("All Papers")
    c.drawString(230,680,"Generated Report")
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)
    textob.textLine("All uploaded papers")
    pdfs = Papers.objects.all()
    lines = []
    c.drawImage("static/img/header.jpg",15,720, width = 650, height = 40)
    header = ['Paper ID','Paper Name','DOI','Paper Location']
    lines.append(header)
    for pdf in pdfs:
        line = []
        line.append(str(pdf.paper_id))
        line.append(pdf.title)
        line.append(pdf.doi)
        line.append(str(pdf.pdf))
        lines.append(line)
    f = Table(lines)
    f.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                             ('ALIGN',(0,0),(-1,-1),'CENTER'),
                             ('FONTSIZE',(0,0),(-1,0),14),
                             ('BOTTOMPADDING',(0,0),(-1,0),12)]))
    f.wrapOn(c,10, 10)
    f.drawOn(c, 50, 500)
    # c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='PapersReport.pdf')
