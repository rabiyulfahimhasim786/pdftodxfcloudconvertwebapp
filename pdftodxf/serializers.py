
from rest_framework import serializers
from .models import urltofile

class Urltofileuploadserializers(serializers.ModelSerializer):
  class Meta:
    model = urltofile
    fields = '__all__'