from django.db import models

# Create your models here.

class urltofile(models.Model):
    pdffilename = models.TextField(null=True, blank=True)
    pdfurl = models.URLField(blank=True)
    pdffilepath = models.TextField(null=True, blank=True)
    dxffilepath = models.TextField(null=True, blank=True)
    dxfurl = models.TextField(null=True, blank=True)