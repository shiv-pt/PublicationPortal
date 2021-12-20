from django.shortcuts import redirect, render
from upload_publication.models import Papers
from django.views.generic import TemplateView
from Userview.models import Issue
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
# Create your views here.


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
        return context

def papersreport(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter)
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)
    textob.textLine("All uploaded papers")
    pdfs = Papers.objects.all()
    lines = []
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
    f.drawOn(c, 50, 650)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='PapersReport.pdf')