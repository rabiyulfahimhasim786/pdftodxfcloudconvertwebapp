from django.urls import path
from . import views
# from .views import (UrltofileuploadView, PdfUpdateDeleteApiView)
from .views import (UrltofileuploadView, PdfUpdateDeleteApiView, pdftodxffileuploadView, pdftodxfUpdateDeleteApiView)

urlpatterns = [
    path('index/', views.index, name='index'),
    path('uploads/', UrltofileuploadView.as_view(), name='file-uploads'),
    path('uploads/<int:pk>/', PdfUpdateDeleteApiView.as_view(), name='pdf-detail'),
    path('pdfuploads/', pdftodxffileuploadView.as_view(), name='pdf-to-dxf-uploads'),
    path('pdfuploads/<int:pk>/', pdftodxfUpdateDeleteApiView.as_view(), name='pdf-to-dxf-detail'),
    # path('site/',views.get_site_name, name='get_site_name'),
    # path('dxfconversions/', views.dxfconversions, name='dxfconversions'),
]