from django.db import models

class Papers(models.Model):
    paper_id = models.DecimalField(max_digits=20, decimal_places=1, primary_key=True)
    title = models.CharField(max_length=100)
    doi = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='papers/pdfs/')
    class Meta:
        db_table = 'paper'
