"""
URL configuration for myfileserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from uploadfile.views import FileUploadView, UploadLocalView, UploadSutrasView, UploadVolumesView,UploadWordAttachmentView,show_upload_file,show_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', FileUploadView.as_view(), name='upload_file'), 
    path('upload_local/', UploadLocalView.as_view(), name='upload_local'),   
    path('upload_attach/', UploadWordAttachmentView.as_view(), name='upload_attach'),
    path('all_volumes/', UploadVolumesView.as_view(), name='all_volumes'),
    path('all_sutras/', UploadSutrasView.as_view(), name='all_sutras'),
    path('index/', show_upload_file, name='index'),
    path('show/', show_file, name='showfile'),
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


 