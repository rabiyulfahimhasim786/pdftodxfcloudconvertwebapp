from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import urltofile, pdftodxffile
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
from .serializers import Urltofileuploadserializers, Pdftodxffileuploadserializers
import requests
import time
import string
import random


# opensource requirements
import subprocess
#dxf conversion
from os import listdir
from os.path import isfile, join
import ezdxf
# Create your views here.
# dotpath = './media/'
# 10 th server

# dotpath = '/var/www/zunamelt.com/pdf.zunamelt.com/media/'
#12 th server

dotpath = '/var/www/subdomain/mirror/htmltopdf/media/' 

dot = f'{dotpath}pdf/'
pdfsplitted_folder_path = "pdfsplit"
pdfsplitfilepath = f'{dotpath}pdfsplit/'
dxffilepath = f'{dotpath}dxf/'
mergeddxffiles = 'merger'
dxf_folder_path =  f'{dotpath}{mergeddxffiles}/'
# dot = './media/pdf/'
# pdfsplitted_folder_path = "pdfsplit"
# pdfsplitfilepath = './media/pdfsplit/'
# dxffilepath = './media/dxf/'

def index(request):
    # files_in = ["page_1.dxf", "page_2.dxf", "page_3.dxf"]
    files_in = []
    dxfconversions(files_in)
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
    while True:
      time.sleep(10)
      firstgetresponse = requests.get(data1, headers=headers)
      print(firstgetresponse.json())
      data2 = firstgetresponse.json()
      verificationurl = data2['data']['links']['self']
      print(verificationurl)
      verificationstatus = data2['data']['status']
      print(verificationstatus)
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
      print(verificationstatus)
      value = dxf_processing(file, verificationurl)
    elif verificationstatus == 'processing':
      print(verificationstatus)
      time.sleep(10)
    #   time.sleep(5)
    #   value = dxf_processing(file, verificationurl)
      if verificationstatus == 'finished':
          print(verificationstatus)
          value = dxf_processing(file, verificationurl)
    elif verificationstatus == 'waiting':
      print(verificationstatus)
      time.sleep(10)
    #   time.sleep(5)
    #   value = dxf_processing(file, verificationurl)
      if verificationstatus == 'finished':
          print(verificationstatus)
          value = dxf_processing(file, verificationurl)
    elif verificationstatus == 'error':
      print(verificationstatus)
      time.sleep(10)
      if verificationstatus == 'finished':
          print(verificationstatus)
          value = dxf_processing(file, verificationurl)
    #   time.sleep(10)
    # #   time.sleep(5)
    #   value = dxf_processing(file, verificationurl)
    else:
      print(verificationstatus)
    #   time.sleep(5)
      time.sleep(10)
    #   value = dxf_processing(file, verificationurl)
      if verificationstatus == 'finished':
          print(verificationstatus)
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
        dxfurlsites = f'{sslname}://{site}/media/{mergeddxffiles}/'
        inputfilesname = 'inputfile'
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['pdfurl']
            pdffilename_file = serializer.validated_data['pdffilename']
            r = requests.get(uploaded_file, stream=True)
            # filename = f'{dotpath}input/{pdffilename_file}.pdf'
            filename = f'{dotpath}input/{inputfilesname}.pdf'
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
            # serializer.save(pdffilepath=pdffilename_file+'.pdf')
            serializer.save(pdffilepath=inputfilesname+'.pdf')
            # pdffilename = []
            pdf_reader = PyPDF2.PdfReader(filename)
            #
            # Loop through each page in the PDF file
            print(len(pdf_reader.pages))
            pdfsplited =[]
            dxffilenamesdata = []
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
                    # staticurl = 'https://trophydeals.com/PrintDxf/3323770_PrintDXf.pdf'
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
                        dxffilenames = f'page_{page_num+1}.dxf'
                        dxffilenamesdata.append(dxffilenames)
                        # pdffilename.append(f'{site_name}page_{page_num+1}.pdf')
                        # print(pdfsplitedurlname)
                        # cloud_convert(pdfsplitedurlname, f'page_{page_num+1}.pdf')
                        with open(pdfsplifilenames, 'wb') as output_file:
                            pdf_writer.write(output_file)
                        time.sleep(1)
                        cloud_convert(pdfsplitedurlname, f'page_{page_num+1}.pdf')
                        
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
                        pdfsplifilenames = pdfsplitfilepath+str(f'page_{page_num+1}.pdf')
                        # Save the current page as a new PDF file
                        pdfsplitedurlname1 = f'{site_name}page_{page_num+1}.pdf'
                        pdffilename.append(pdfsplitedurlname1)
                        dxffilenames = f'page_{page_num+1}.dxf'
                        dxffilenamesdata.append(dxffilenames)
                        # pdffilename.append(pdfsplifilenames)
                        # pdffilename.append(f'{site_name}page_{page_num+1}.pdf')
                        # cloud_convert(pdfsplitedurlname, f'page_{page_num+1}.pdf')
                        with open(pdfsplifilenames, 'wb') as output_file:
                            pdf_writer.write(output_file)
                        time.sleep(2)
                        cloud_convert(pdfsplitedurlname1, f'page_{page_num+1}.pdf')
                        
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
            pdffilemesssages = 'Your pdf files splitted succesfully'
            dxffilenamesserver = dxfconversions(dxffilenamesdata)
            file_out = "merge.dxf"
            # dxfurl = f'{dxfurlsites}{dxffilenamesserver}'
            dxfurl = f'{dxfurlsites}{file_out}'
            serializer.save(dxfurl=dxfurl, dxffilepath=dxffilenamesserver, pdffilepath=pdffilemesssages)
           
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




# def dxfconversions(pdffilename):
#   if pdffilename==[]:
#       pass
#   else:
#     # Input Directory
#     path_in = dotpath+"dxf/"
#     # path_in = "in/"
#     # Input files
#     # files_in = ["page_1.dxf", "page_2.dxf", "page_3.dxf", "page_4.dxf"]
#     # files_in = ["page_1.dxf", "page_2.dxf", "page_3.dxf"]
#     files_in = pdffilename
#     # Output Directory
#     # path_out = dotpath+"merger/"
#     path_out = dxf_folder_path
#     # path_out = "out/"
#     # Output file
#     file_out = "merge.dxf"
#     """
#     use_file_list 
#     ( If it's set to True, will use the hardcoded dxf files from 'files_in'
#     If it's set to False, will use all dxf files in 'path_in' directory
#     Default is True )
#     """
#     use_file_list = True

#     if not use_file_list:
#         files_in = [
#             f
#             for f in listdir(path_in)
#             if isfile(join(path_in, f))
#             if f.lower().endswith(".dxf")
#         ]

#     # empty target dxf
#     target_dxf = ezdxf.new("R2000")

#     # Define the offset for each input DXF file
#     offset_x = 0.0
#     offset_y = 0.0
#     max_height = 0

#     # merger with filelist
#     for filename in files_in:
#         # path prepare
#         print("input  ->", filename)
#         pathfilename = path_in + filename
#         filenoext = filename.split(".")[0]

#         append_dxf = ezdxf.readfile(pathfilename)

#         # Get the modelspace of the input file
#         modelspace = append_dxf.modelspace()

#         # Calculate the height of the DXF file
#         for entity in modelspace:
#             if entity.dxftype() == 'LINE':
#                 start = entity.dxf.start
#                 if max_height < start[1]:
#                     max_height = start[1]
#                 end = entity.dxf.end
#                 if max_height < end[1]:
#                     max_height = end[1]
#             elif entity.dxftype() == 'SPLINE':
#                 control_points = entity._control_points
#                 for item in control_points:
#                     if max_height < item[1]:
#                         max_height = item[1]
#             elif entity.dxftype() == 'CIRCLE' or entity.dxftype() == 'ARC' or entity.dxftype() == 'ELLIPSE':
#                 center = entity.dxf.center
#                 if max_height < center[1] * 2:
#                     max_height = center[1] * 2
#             elif entity.dxftype() == 'POLYLINE':
#                 points = entity.points()
#                 for item in points:
#                     if max_height < item[1]:
#                         max_height = item[1]
#             else:
#                 if max_height < 30:
#                     max_height = 30

#         # Create new block definition for the input file
#         block_def = target_dxf.blocks.new(name=filename)

#         # Iterate over each entity in the modelspace
#         for entity in modelspace:
#             # Copy the entity to the new block definition
#             block_def.add_entity(entity.copy())

#         # Create an insert entity for the block definition
#         target_dxf.modelspace().add_blockref(
#             name=filename,
#             insert=(offset_x, offset_y),
#             dxfattribs={
#                 "xscale": 1.0,
#                 "yscale": 1.0,
#                 "rotation": 0.0,
#             }
#         )

#         # Increment the offset for the next file
#         offset_y -= (max_height * 1.2)

#     # save merged dfx target
#     try:
#         print("target ->", file_out)
#         message = file_out
#         target_dxf.saveas(path_out + file_out)
#     except Exception as e:
#         print("Error -> ", e.__class__)
#         message =  e.__class__

#   # return HttpResponse('Hello world')
# #   return "ok"
#     return file_out
  


def dxfconversions(pdffilename):
  if pdffilename==[]:
      pass
  else:
    # Input Directory
    path_in = dotpath+"dxf/"
    # path_in = "in/"
    # Input files
    # files_in = ["page_1.dxf", "page_2.dxf", "page_3.dxf", "page_4.dxf"]
    # files_in = ["page_1.dxf", "page_2.dxf", "page_3.dxf"]
    files_in = pdffilename
    # Output Directory
    # path_out = dotpath+"merger/"
    path_out = dxf_folder_path
    # path_out = "out/"
    # Output file
    file_out = "merge.dxf"
    """
    use_file_list 
    ( If it's set to True, will use the hardcoded dxf files from 'files_in'
    If it's set to False, will use all dxf files in 'path_in' directory
    Default is True )
    """
    use_file_list = True
    dxffile_messages = ''
    if not use_file_list:
        files_in = [
            f
            for f in listdir(path_in)
            if isfile(join(path_in, f))
            if f.lower().endswith(".dxf")
        ]

    # empty target dxf
    target_dxf = ezdxf.new("R2000")

    # Define the offset for each input DXF file
    offset_x = 0.0
    offset_y = 0.0
    max_height = 0

    # merger with filelist
    for filename in files_in:
        try:
            # path prepare
            print("input  ->", filename)
            pathfilename = path_in + filename
            filenoext = filename.split(".")[0]

            append_dxf = ezdxf.readfile(pathfilename)

            # Get the modelspace of the input file
            modelspace = append_dxf.modelspace()

            # Calculate the height of the DXF file
            for entity in modelspace:
                if entity.dxftype() == 'LINE':
                    start = entity.dxf.start
                    if max_height < start[1]:
                        max_height = start[1]
                    end = entity.dxf.end
                    if max_height < end[1]:
                        max_height = end[1]
                elif entity.dxftype() == 'SPLINE':
                    control_points = entity._control_points
                    for item in control_points:
                        if max_height < item[1]:
                            max_height = item[1]
                elif entity.dxftype() == 'CIRCLE' or entity.dxftype() == 'ARC' or entity.dxftype() == 'ELLIPSE':
                    center = entity.dxf.center
                    if max_height < center[1] * 2:
                        max_height = center[1] * 2
                elif entity.dxftype() == 'POLYLINE':
                    points = entity.points()
                    for item in points:
                        if max_height < item[1]:
                            max_height = item[1]
                else:
                    if max_height < 30:
                        max_height = 30

            # Create new block definition for the input file
            block_def = target_dxf.blocks.new(name=filename)

            # Iterate over each entity in the modelspace
            for entity in modelspace:
                # Copy the entity to the new block definition
                block_def.add_entity(entity.copy())

            # Create an insert entity for the block definition
            target_dxf.modelspace().add_blockref(
                name=filename,
                insert=(offset_x, offset_y),
                dxfattribs={
                    "xscale": 1.0,
                    "yscale": 1.0,
                    "rotation": 0.0,
                }
            )

            # Increment the offset for the next file
            offset_y -= (max_height * 1.2)
            dxffile_messages = f"Dxf file successfully merged"
        except IOError:
            dxffile_messages = f"Not a DXF file or a generic I/O error."
        except ezdxf.DXFStructureError:
            dxffile_messages = f"Invalid or corrupted DXF file."
        except Exception as e:
            dxffile_messages = f"Error -> {e.__class__}"
    print(dxffile_messages)

    # save merged dfx target
    try:
        print("target ->", file_out)
        message = file_out
        target_dxf.saveas(path_out + file_out)
    except Exception as e:
        print("Error -> ", e.__class__)
        message =  e.__class__

  # return HttpResponse('Hello world')
#   return "ok"
    # return file_out
    return dxffile_messages

class PdfUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = urltofile.objects.all()
    serializer_class = Urltofileuploadserializers
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]



def pdftodxfconversionprocess(filenames):
    print(filenames)
    # Save the current page as a new PDF file
    # pdfsplitfilenames = pdftodxffilepath+str(f'page_{1}.pdf')
    # dxfsplitfilenames = pdftodxffilepath+str(f'page_{1}.dxf')
    # command = ["pstoedit", "-f", "dxf: -ctl -mm", "input.pdf", "input.dxf"]
    # command = ["pstoedit", "-f", "dxf: -ctl -mm", pdfsplitfilenames, dxfsplitfilenames]
    # pdfsplitfilenames = pdftodxffilepath+str(f'{filenames}.pdf')
    # dxfsplitfilenames = pdftodxffilepath+str(f'{filenames}.dxf')
    pdfsplitfilenames = pdfsplitfilepath+str(f'{filenames}.pdf')
    dxfsplitfilenames = dxffilepath+str(f'{filenames}.dxf')
    command = ["pstoedit", "-f", "dxf: -ctl -mm", pdfsplitfilenames, dxfsplitfilenames]
    
    try:
        subprocess.run(command, check=True) # Raise an exeption if the command fails
        messages = "Conversion Succesful"
    # except subprocess.CalledprocessError as error:
    #     messages = f"Conversion failed with error: {error}"
    except Exception as e:
        messages = f"Conversion failed with error: {e}"

    print(messages)
    return 'ok'




def pdftodxfconversions(pdffilename):
  if pdffilename==[]:
      pass
  else:
    # Input Directory
    # path_in = dotpath+"pdftodxf/"
    path_in = dxffilepath
    # path_in = "in/"
    # Input files
    # files_in = ["page_1.dxf", "page_2.dxf", "page_3.dxf", "page_4.dxf"]
    # files_in = ["page_1.dxf", "page_2.dxf", "page_3.dxf"]
    #files_in = ["shape.dxf", "input.dxf"]
    files_in = pdffilename
    # Output Directory
    # path_out = dotpath+"merger/"
    path_out = dxf_folder_path
    # path_out = "out/"
    # Output file
    file_out = "merge.dxf"
    """
    use_file_list 
    ( If it's set to True, will use the hardcoded dxf files from 'files_in'
    If it's set to False, will use all dxf files in 'path_in' directory
    Default is True )
    """
    use_file_list = True
    dxffile_messages = ''
    if not use_file_list:
        files_in = [
            f
            for f in listdir(path_in)
            if isfile(join(path_in, f))
            if f.lower().endswith(".dxf")
        ]

    # empty target dxf
    target_dxf = ezdxf.new("R2000")

    # Define the offset for each input DXF file
    offset_x = 0.0
    offset_y = 0.0

    # merger with filelist
    for filename in files_in:
        max_height = 0.0
        min_height = 10000.0
        try:
            # path prepare
            print("input  ->", filename)
            pathfilename = path_in + filename
            filenoext = filename.split(".")[0]

            append_dxf = ezdxf.readfile(pathfilename)

            # Get the modelspace of the input file
            modelspace = append_dxf.modelspace()

            # Calculate the height of the DXF file
            for entity in modelspace:
                block_name = f"{filename}_{entity.dxf.handle}"
                block_def = target_dxf.blocks.new(name=block_name)
                block_def.add_entity(entity.copy())
                
                # Create a separate insert entity for each entity in the modelspace
                insert_entity = target_dxf.modelspace().add_blockref(
                    name=block_name,
                    insert=(offset_x, offset_y),
                    dxfattribs={
                        "xscale": 1.0,
                        "yscale": 1.0,
                        "rotation": 0.0,
                    }
                )
                # Each insert entity represents an individual entity in the merged DXF file
                # Make each insert entity unique by setting its handle to the entity's handle
                # insert_entity.set_handle(entity.dxf.handle)
                
                if entity.dxftype() == 'LINE':
                    start = entity.dxf.start
                    if max_height < start[1]:
                        max_height = start[1]
                    if min_height > start[1]:
                        min_height = start[1]
                    end = entity.dxf.end
                    if max_height < end[1]:
                        max_height = end[1]
                    if min_height > end[1]:
                        min_height = end[1]
                elif entity.dxftype() == 'SPLINE':
                    control_points = entity._control_points
                    for item in control_points:
                        if max_height < item[1]:
                            max_height = item[1]
                        if min_height > item[1]:
                            min_height = item[1]
                elif entity.dxftype() == 'CIRCLE' or entity.dxftype() == 'ARC' or entity.dxftype() == 'ELLIPSE':
                    center = entity.dxf.center
                    if max_height < center[1] + entity.dxf.radius:
                        max_height = center[1] + entity.dxf.radius
                    if min_height > center[1] + entity.dxf.radius:
                        min_height = center[1] + entity.dxf.radius
                elif entity.dxftype() == 'POLYLINE':
                    points = entity.points()
                    for item in points:
                        if max_height < item[1]:
                            max_height = item[1]
                        if min_height > item[1]:
                            min_height = item[1]
                else:
                    if max_height < 30:
                        max_height = 30
                    if min_height == 10000.0:
                        min_height = 0

            # Increment the offset for the next file
            offset_y -= (max_height - min_height) * 1.5
            dxffile_messages = f"Dxf file successfully merged"
        except IOError:
            dxffile_messages = f"Not a DXF file or a generic I/O error."
        except ezdxf.DXFStructureError:
            dxffile_messages = f"Invalid or corrupted DXF file."
        except Exception as e:
            dxffile_messages = f"Error -> {e.__class__}"
            
    print(dxffile_messages)

    # save merged dfx target
    try:
        print("target ->", file_out)
        message = file_out
        target_dxf.saveas(path_out + file_out)
    except Exception as e:
        print("Error -> ", e.__class__)
        message =  e.__class__

  # return HttpResponse('Hello world')
#   return "ok"
    # return file_out
    return dxffile_messages



class pdftodxffileuploadView(ListCreateAPIView):
    queryset = pdftodxffile.objects.all()
    serializer_class = Pdftodxffileuploadserializers
   
    def perform_create(self, serializer):
        sslname =   self.request.scheme    
        site = self.request.META['HTTP_HOST']
          # site_name = "{}".format(request.META['HTTP_HOST'])
        site_name = f'{sslname}://{site}/media/{pdfsplitted_folder_path}/'
        dxfurlsites = f'{sslname}://{site}/media/{mergeddxffiles}/'
        inputfilesname = 'inputfile'
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['pdfurl']
            pdffilename_file = serializer.validated_data['pdffilename']
            r = requests.get(uploaded_file, stream=True)
            # filename = f'{dotpath}input/{pdffilename_file}.pdf'
            filename = f'{dotpath}input/{inputfilesname}.pdf'
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
            # serializer.save(pdffilepath=pdffilename_file+'.pdf')
            serializer.save(pdffilepath=inputfilesname+'.pdf')
            # pdffilename = []
            pdf_reader = PyPDF2.PdfReader(filename)
            #
            # Loop through each page in the PDF file
            print(len(pdf_reader.pages))
            pdfsplited =[]
            dxffilenamesdata = []
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
                    # staticurl = 'https://trophydeals.com/PrintDxf/3323770_PrintDXf.pdf'
                    for page_num in range(len(pdf_reader.pages)):
                        # Create a new PDF writer object
                        pdf_writer = PyPDF2.PdfWriter()

                        # Add the current page to the PDF writer object
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                
                        # Save the current page as a new PDF file
                        pdfsplifilenames = pdfsplitfilepath+str(f'page_{page_num+1}.pdf')
                        # pdffilename.append(pdfsplifilenames)
                        pdfsplitedurlname = f'{site_name}page_{page_num+1}.pdf'
                        pdffileprocess = f'page_{page_num+1}'
                        pdffilename.append(pdfsplitedurlname)
                        dxffilenames = f'page_{page_num+1}.dxf'
                        dxffilenamesdata.append(dxffilenames)
                        # pdffilename.append(f'{site_name}page_{page_num+1}.pdf')
                        # print(pdfsplitedurlname)
                        # cloud_convert(pdfsplitedurlname, f'page_{page_num+1}.pdf')
                        with open(pdfsplifilenames, 'wb') as output_file:
                            pdf_writer.write(output_file)
                        time.sleep(1)
                        # cloud_convert(pdfsplitedurlname, f'page_{page_num+1}.pdf')
                        pdftodxfconversionprocess(pdffileprocess)
                        
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
                        pdfsplifilenames = pdfsplitfilepath+str(f'page_{page_num+1}.pdf')
                        # Save the current page as a new PDF file
                        pdfsplitedurlname1 = f'{site_name}page_{page_num+1}.pdf'
                        pdffileprocess = f'page_{page_num+1}'
                        pdffilename.append(pdfsplitedurlname1)
                        dxffilenames = f'page_{page_num+1}.dxf'
                        dxffilenamesdata.append(dxffilenames)
                        # pdffilename.append(pdfsplifilenames)
                        # pdffilename.append(f'{site_name}page_{page_num+1}.pdf')
                        # cloud_convert(pdfsplitedurlname, f'page_{page_num+1}.pdf')
                        with open(pdfsplifilenames, 'wb') as output_file:
                            pdf_writer.write(output_file)
                        time.sleep(2)
                        # cloud_convert(pdfsplitedurlname1, f'page_{page_num+1}.pdf')
                        pdftodxfconversionprocess(pdffileprocess)
                        
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
            pdffilemesssages = 'Your pdf files splitted succesfully'
            # dxffilenamesserver = dxfconversions(dxffilenamesdata)
            dxffilenamesserver = pdftodxfconversions(dxffilenamesdata)
            file_out = "merge.dxf"
            # dxfurl = f'{dxfurlsites}{dxffilenamesserver}'
            dxfurl = f'{dxfurlsites}{file_out}'
            serializer.save(dxfurl=dxfurl, dxffilepath=dxffilenamesserver, pdffilepath=pdffilemesssages)
           
        # return pdfsplited
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class pdftodxfUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = pdftodxffile.objects.all()
    serializer_class = Pdftodxffileuploadserializers
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

