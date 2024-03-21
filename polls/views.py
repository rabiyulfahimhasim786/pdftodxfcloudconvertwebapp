#from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from rest_framework.response import Response
from .serializers import PdfSerializer,Htmltopdffileuploadserializers#, StandardsSerializer, CountriesSerializer, TagSerializer

from .models import Pdf,htmltopdffile#, Standards, Countries, Tag

from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.views import APIView
# from rest_framework import status
# Create your views here.
from django.http import HttpResponse
# Create your views here.
from django.http import HttpResponse

import img2pdf
from PIL import Image
import os
import pdfkit
import imgkit
import time
import requests
auth = 'yourcloudconverauth-key'
def index(request):
    return HttpResponse("Hello, world!")

# dotpath = './media/'
dotpath = '/var/www/subdomain/mirror/htmltopdf/media/'
# basedotpath = f'.'
# basedotpath = f'/var/www/subdomain/mirror/htmltopdf/'
# pdffilespath = f'{basedotpath}pdf/'
pdffilespath = 'pdf'
pdflocalpath = f'{dotpath}{pdffilespath}/'
class PdfList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        currencies = Pdf.objects.all()
        serializer = PdfSerializer(currencies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PdfSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PdfDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Pdf.objects.get(pk=pk)
        except Pdf.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        currencies = self.get_object(pk)
        serializer = PdfSerializer(currencies)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        currencies = self.get_object(pk)
        serializer = PdfSerializer(currencies, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



def pdfurl(request):
    documents = Pdf.objects.all()
    #rank = Document.objects.latest('id')
    #print(rank)
    for obj in documents:
        rank = obj.link
        num  =  obj.name
        #print(rank)
    #print(rank[8:-5])
    #print('/media/'+rank[8:-5]+'.pdf')
    #pdfkit.from_url(rank, './media/pdf/'+str(num)+'.pdf')
    # pdfkit.from_url(rank, '/var/www/mirror/htmltopdf/media/pdf/'+num+'.pdf')
    # pdfkit.from_url(rank, f'{dotpath}pdf/'+num+'.pdf')#working code # 14/2/2024 bug raises
    # pdfkit.from_url(str(rank), f'{dotpath}pdf/'+str(num)+'.pdf', options={"enable-local-file-access": ""})
    try:
        pdfkit.from_url(rank, f'{dotpath}pdf/'+str(num)+'.pdf')
    except:
        pass
    return HttpResponse("Hello, world!")



def imgurl(request):
    documents = Pdf.objects.all()
    #rank = Document.objects.latest('id')
    #print(rank)
    for obj in documents:
        img = obj.link
        numb = obj.number
        #print(img)
    #print(img[8:-5])
    #print('/media/'+img[8:-5]+'.jpg')
    # imgkit.from_url(img, './media/img/'+str(numb)+'.jpg')
    imgkit.from_url(img, f'{dotpath}img/'+str(numb)+'.jpg')
    #return HttpResponse("Hello, world!")
    return redirect('imgtopdf')


def imgtopdf(request):
    documents = Pdf.objects.all()
    #rank = Document.objects.latest('id')
    #print(rank)
    for obj in documents:
        img = obj.link
        numb = obj.number
        #print(img)
    #print(img[8:-5])
    #print('/media/'+img[8:-5]+'.jpg')
    #imgkit.from_url(img, './media/img/'+str(numb)+'.jpg')
    # img_path =  './media/img/'+str(numb)+'.jpg'
    img_path =  f'{dotpath}img/'+str(numb)+'.jpg'
    # storing pdf path
    # pdf_path = './media/img/'+str(numb)+'.pdf'
    pdf_path = f'{dotpath}img/'+str(numb)+'.pdf'

    # opening image
    image = Image.open(img_path)

    # converting into chunks using img2pdf
    pdf_bytes = img2pdf.convert(image.filename)

    # opening or creating pdf file 
    file = open(pdf_path, "wb")

    # writing pdf files with chunks
    file.write(pdf_bytes)

    # closing image file
    image.close()

    # closing pdf file
    file.close()
    return HttpResponse("Hello, world!")

#cloud convert process
#1
def dxf_processing(file, verificationurl):
  auth_token= auth
  headers = {'Authorization': f'Bearer {auth_token}'}
  secondgetresponse = requests.get(f'{verificationurl}?redirect=true', headers=headers, )
  # Download the output DXF file.
  # dxffilename = file.replace('.html', '')
  # dxffilename = file.replace('.html', '')
  #dynamicname
#   dxffilename = file
  #static name
  dxffilename = 'merge'
  output_dxf_file_name = pdflocalpath+str(f'{dxffilename}.pdf')
#   output_dxf_file_name = str(f'{dxffilename}.pdf')
  output_dxf_file = open(output_dxf_file_name, 'wb')
  output_dxf_file.write(secondgetresponse.content)
  output_dxf_file.close()
#   print(file)
  return 'ok'
#2

def cloud_convert(pdfurl, file):
    auth_token= auth
    headers = {'Authorization': f'Bearer {auth_token}'}
    data = {
      "tasks": {
        "import-my-file": {
          "operation": "import/url",
          "url": pdfurl
        },
        "convert-my-file": {
          "operation": "convert",
          "input": "import-my-file",
          "input_format": "html",
          "output_format": "pdf"
        },
        "export-my-file": {
          "operation": "export/url",
          "input": "convert-my-file"
        }
      }
    }

    url = 'https://api.cloudconvert.com/v2/jobs'
    response = requests.post(url, json=data, headers=headers)
    # print(response)
    # print(response.json())
    data = response.json()
    data1 = data['data']['links']['self']
    while True:
      time.sleep(10)
      firstgetresponse = requests.get(data1, headers=headers)
    #   print(firstgetresponse.json())
      data2 = firstgetresponse.json()
      verificationurl = data2['data']['links']['self']
    #   print(verificationurl)
      verificationstatus = data2['data']['status']
    #   print(verificationstatus)
      if verificationstatus == 'finished':
        break
    # firstgetresponse = requests.get(data1, headers=headers)
    # print(firstgetresponse.json())
    # data2 = firstgetresponse.json()
    # verificationurl = data2['data']['links']['self']
    # print(verificationurl)
    # verificationstatus = data2['data']['status']
    # print(verificationstatus)
    if verificationstatus == 'finished':
    #   print(verificationstatus)
      value = dxf_processing(file, verificationurl)
    elif verificationstatus == 'processing':
    #   print(verificationstatus)
      time.sleep(10)
    #   time.sleep(5)
    #   value = dxf_processing(file, verificationurl)
      if verificationstatus == 'finished':
          print(verificationstatus)
          value = dxf_processing(file, verificationurl)
    elif verificationstatus == 'waiting':
    #   print(verificationstatus)
      time.sleep(10)
    #   time.sleep(5)
    #   value = dxf_processing(file, verificationurl)
      if verificationstatus == 'finished':
          print(verificationstatus)
          value = dxf_processing(file, verificationurl)
    elif verificationstatus == 'error':
    #   print(verificationstatus)
      time.sleep(10)
      if verificationstatus == 'finished':
        #   print(verificationstatus)
          value = dxf_processing(file, verificationurl)
    #   time.sleep(10)
    # #   time.sleep(5)
    #   value = dxf_processing(file, verificationurl)
    else:
    #   print(verificationstatus)
    #   time.sleep(5)
      time.sleep(10)
    #   value = dxf_processing(file, verificationurl)
      if verificationstatus == 'finished':
        #   print(verificationstatus)
          value = dxf_processing(file, verificationurl)
    return 'ok'

class htmltopdffileuploadView(ListCreateAPIView):
    queryset = htmltopdffile.objects.all()
    serializer_class = Htmltopdffileuploadserializers
   
    def perform_create(self, serializer):
        sslname =   self.request.scheme    
        site = self.request.META['HTTP_HOST']
          # site_name = "{}".format(request.META['HTTP_HOST'])
        # site_name = f'{sslname}://{site}/media/{pdfsplitted_folder_path}/'
        dxfurlsites = f'{sslname}://{site}/media/{pdffilespath}/'
        inputfilesname = 'inputfile'
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['htmlurl']
            pdffilename_file = serializer.validated_data['htmlfilename']
            pdfcloudconvert = cloud_convert(uploaded_file, pdffilename_file)
            pdffilemesssages = 'Your html files converted as pdf succesfully'
            # dxffilenamesserver = dxfconversions(dxffilenamesdata)
            # dxffilenamesserver = pdftodxfconversions(dxffilenamesdata)
            dxffilenamesserver = 'Your html files loaded succesfully'
            file_out = "merge.pdf"
            # dxfurl = f'{dxfurlsites}{dxffilenamesserver}'
            dxfurl = f'{dxfurlsites}{file_out}'
            serializer.save(pdfurl=dxfurl, htmlfilepath=dxffilenamesserver, pdffilepath=pdffilemesssages)
           
        # return pdfsplited
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class htmltopdfUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = htmltopdffile.objects.all()
    serializer_class = Htmltopdffileuploadserializers
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

