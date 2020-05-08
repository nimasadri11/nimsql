"""videoplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from videoplatform.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404

handler404 = 'videoplatform.views.error404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SubscribeWizard.as_view([SubscribeForm1, SubscribeForm2, SubscribeForm3])),
    path('signup/', signup),
    path('login/', signin),
    path('logout/', logoutUser),
    path('videos/', VideoView.as_view()),
    path('play/', play),
    path('change_password/', change_password),
    path('account/', account),
    path('creator/<slug:name>', CreatorVideoView.as_view()),
    path('dashboard/', dashboard_analytics),
    path('dashboard/upload', dashboard_upload),
    path('dashboard/manage', dashboard_manage),
    path('dashboard/manage/video', dashboard_manage_video),
    path('dashboard/manage/video/delete', delete_video),
    path('dashboard/support', dashboard_support),
    path('contact/', SubscribeWizard.as_view([SubscribeForm1, SubscribeForm2])),
    path('join/', SubscribeWizard.as_view([SubscribeForm1, SubscribeForm2])),

    
    
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

