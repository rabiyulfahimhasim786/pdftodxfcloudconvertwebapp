from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import urltofile
from rest_framework.response import Response
from django.shortcuts import render,redirect
import PyPDF2

from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
from django.core.files.storage import default_storage
from .serializers import Urltofileuploadserializers
import requests
import time
import string
import random


#dxf conversion
from os import listdir
from os.path import isfile, join
import ezdxf
# Create your views here.
dotpath = './media/'
dot = './media/pdf/'
pdfsplitted_folder_path = "pdfsplit"
pdfsplitfilepath = './media/pdfsplit/'
dxffilepath = './media/dxf/'

def index(request):
    return HttpResponse('Hello World')

auth = 'your cloud convert auth token'
def dxf_processing(file, verificationurl):
  auth_token= auth
  headers = {'Authorization': f'Bearer {auth_token}'}
  secondgetresponse = requests.get(f'{verificationurl}?redirect=true', headers=headers, )
  # Download the output DXF file.
  dxffilename = file.replace('.pdf', '')
  output_dxf_file_name = dxffilepath+str(f'{dxffilename}.dxf')
  output_dxf_file = open(output_dxf_file_name, 'wb')
  output_dxf_file.write(secondgetresponse.content)
  output_dxf_file.close()
  print(file)
  return 'ok'

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
          "input_format": "pdf",
          "output_format": "dxf"
        },
        "export-my-file": {
          "operation": "export/url",
          "input": "convert-my-file"
        }
      }
    }

    url = 'https://api.cloudconvert.com/v2/jobs'
    response = requests.post(url, json=data, headers=headers)
    print(response)
    print(response.json())
    data = response.json()
    data1 = data['data']['links']['self']
    firstgetresponse = requests.get(data1, headers=headers)
    print(firstgetresponse.json())
    data2 = firstgetresponse.json()
    verificationurl = data2['data']['links']['self']
    print(verificationurl)
    verificationstatus = data2['data']['status']
    print(verificationstatus)
    if verificationstatus == 'finished':
      print(verificationstatus)
      value = dxf_processing(file, verificationurl)
    elif verificationstatus == 'processing':
      print(verificationstatus)
      time.sleep(10)
      value = dxf_processing(file, verificationurl)
    elif verificationstatus == 'waiting':
      print(verificationstatus)
      time.sleep(10)
      value = dxf_processing(file, verificationurl)
    else:
      print(verificationstatus)
      time.sleep(10)
      value = dxf_processing(file, verificationurl)
    return 'ok'


class UrltofileuploadView(ListCreateAPIView):
    queryset = urltofile.objects.all()
    serializer_class = Urltofileuploadserializers
   
    def perform_create(self, serializer):
        sslname =   self.request.scheme    
        site = self.request.META['HTTP_HOST']
          # site_name = "{}".format(request.META['HTTP_HOST'])
        site_name = f'{sslname}://{site}/media/{pdfsplitted_folder_path}/'
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['pdfurl']
            pdffilename_file = serializer.validated_data['pdffilename']
            r = requests.get(uploaded_file, stream=True)
            filename = f'{dotpath}input/{pdffilename_file}.pdf'
            with open(filename, 'wb') as f:
                f.write(r.content)
            # uploaded_file = Pdffileuplaodsserilaizers(pdffile=request.pdffile)
            # uploaded_file = self.request.data.get('pdffile', None)
            # serializer = Pdffileuplaodsserilaizers(data=request.data)
            print(uploaded_file)
            # with uploaded_file.open('rb') as file:
            #     pdf = PyPDF2.PdfReader(file)
            #     pages = len(pdf.pages)
            # filepath = dot+str(uploaded_file)
            serializer.save(pdffilepath=pdffilename_file+'.pdf')
            # pdffilename = []
            pdf_reader = PyPDF2.PdfReader(filename)
            #
            # Loop through each page in the PDF file
            print(len(pdf_reader.pages))
            pdfsplited =[]
            if int(len(pdf_reader.pages)) ==1:
                # print(len(pdf_reader.pages), 'if')
                pdffilename = []
                # print(len(pdf_reader.pages), 'else')
                with open(filename, 'rb') as pdf_file:
                    # Create a PDF reader object
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    # pdfurlslist = []
                    # Loop through each page in the PDF file
                    print(len(pdf_reader.pages))
                    staticurl = 'https://trophydeals.com/PrintDxf/3323770_PrintDXf.pdf'
                    for page_num in range(len(pdf_reader.pages)):
                        # Create a new PDF writer object
                        pdf_writer = PyPDF2.PdfWriter()

                        # Add the current page to the PDF writer object
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                
                        # Save the current page as a new PDF file
                        pdfsplifilenames = pdfsplitfilepath+str(f'page_{page_num+1}.pdf')
                        # pdffilename.append(pdfsplifilenames)
                        pdfsplitedurlname = f'{site_name}page_{page_num+1}.pdf'
                        pdffilename.append(pdfsplitedurlname)
                        # pdffilename.append(f'{site_name}page_{page_num+1}.pdf')
                        print(pdfsplitedurlname)
                        # cloud_convert(staticurl, f'page_{page_num+1}.pdf')
                        with open(pdfsplifilenames, 'wb') as output_file:
                            pdf_writer.write(output_file)
                        
                # Save the number of pages to the model, you might want to customize this
                # serializer.save(pdfsplited=','.join(pdffilename))
                pdfsplited=','.join(pdffilename)
                pass
            elif int(len(pdf_reader.pages)) ==0:
                # print(len(pdf_reader.pages), 'elif')
                pass
            else:
                pdffilename = []
                # print(len(pdf_reader.pages), 'else')
                with open(filename, 'rb') as pdf_file:
                    # Create a PDF reader object
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    # pdfurlslist = []
                    # Loop through each page in the PDF file
                    print(len(pdf_reader.pages))
                    for page_num in range(len(pdf_reader.pages)):
                        # Create a new PDF writer object
                        pdf_writer = PyPDF2.PdfWriter()

                        # Add the current page to the PDF writer object
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                
                        # Save the current page as a new PDF file
                        pdfsplifilenames = pdfsplitfilepath+str(f'page_{page_num+1}.pdf')
                        # pdffilename.append(pdfsplifilenames)
                        # pdffilename.append(f'{site_name}page_{page_num+1}.pdf')
                        with open(pdfsplifilenames, 'wb') as output_file:
                            pdf_writer.write(output_file)
                        
                # Save the number of pages to the model, you might want to customize this
                # serializer.save(pdfsplited=','.join(pdffilename))
                pdfsplited=','.join(pdffilename)
                pass
            # with open(filepath, 'rb') as pdf_file:
            #     # Create a PDF reader object
            #     pdf_reader = PyPDF2.PdfReader(pdf_file)
            #     # pdfurlslist = []
            #     # Loop through each page in the PDF file
            #     print(len(pdf_reader.pages))
            #     for page_num in range(len(pdf_reader.pages)):
            #         # Create a new PDF writer object
            #         pdf_writer = PyPDF2.PdfWriter()

            #         # Add the current page to the PDF writer object
            #         pdf_writer.add_page(pdf_reader.pages[page_num])
            
            #         # Save the current page as a new PDF file
            #         pdfsplifilenames = pdfsplitfilepath+str(f'page_{page_num+1}.pdf')
            #         # pdffilename.append(pdfsplifilenames)
            #         pdffilename.append(f'{site_name}page_{page_num+1}.pdf')
            #         with open(pdfsplifilenames, 'wb') as output_file:
            #             pdf_writer.write(output_file)
                       
            # # Save the number of pages to the model, you might want to customize this
            # serializer.save(dxffile=','.join(pdffilename))

        # return pdfsplited
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # def post(self, request, *args, **kwargs):
    #     response = super().post(request, *args, **kwargs)
    #     if response.status_code == 201:  # Check if the file was successfully created
    #         pages = self.perform_create(self.get_serializer(data=request.data))
    #         return Response({'pages': pages}, status=201)
    #     return response