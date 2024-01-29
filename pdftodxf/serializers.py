
from rest_framework import serializers
from .models import urltofile, pdftodxffile

class Urltofileuploadserializers(serializers.ModelSerializer):
  class Meta:
    model = urltofile
    fields = '__all__'


class Pdftodxffileuploadserializers(serializers.ModelSerializer):
  class Meta:
    model = pdftodxffile
    fields = '__all__'