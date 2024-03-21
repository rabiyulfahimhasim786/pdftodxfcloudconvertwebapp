from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import (htmltopdffileuploadView, htmltopdfUpdateDeleteApiView)

urlpatterns = [
    path('', views.index, name='index'),
    path('pdfurl/', views.pdfurl, name='pdfurl'),
    path('imgurl/', views.imgurl, name='imgurl'),
    path('imgtopdf/', views.imgtopdf, name='imgtopdf'),
    path('pdf/', views.PdfList.as_view()),
    path('pdf/<int:pk>/', views.PdfDetail.as_view()),
    path('htmluploads/', htmltopdffileuploadView.as_view(), name='html-to-pdf-uploads'),
    path('htmluploads/<int:pk>/', htmltopdfUpdateDeleteApiView.as_view(), name='html-to-pdf-detail'),
    #path('fileuploading/', views.uploadings, name='uploadings'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
