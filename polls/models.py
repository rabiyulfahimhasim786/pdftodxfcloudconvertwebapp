from django.db import models

# Create your models here.
class Pdf(models.Model):
    link = models.URLField(max_length=255)
    #iso = models.IntegerField()
    #description = models.CharField(max_length=10)
    
    def __str__(self):
        return "%s" % (self.link)