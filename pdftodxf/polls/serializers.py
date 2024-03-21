from rest_framework import serializers
from .models import Pdf, htmltopdffile

class PdfSerializer(serializers.ModelSerializer):
  class Meta:
    model = Pdf
    fields = '__all__'




class Htmltopdffileuploadserializers(serializers.ModelSerializer):
  class Meta:
    model = htmltopdffile
    fields = '__all__'