from django.shortcuts import render
from upload_publication.models import Papers

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
# Create your views here.
def papersreport(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)
    pdfs = Papers.objects.all()
    lines1 = [
        "This is line 1",
        "This is line 2",
        "This is line 3"
    ]
    lines = []
    for pdf in pdfs:
        lines.append(str(pdf.paper_id))
        lines.append(pdf.title)
        lines.append(pdf.doi)
        lines.append(str(pdf.pdf))
        lines.append(" ")
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='PapersReport.pdf')
    #return render(request, 'showpdf.html', {'pdfs': pdfs})