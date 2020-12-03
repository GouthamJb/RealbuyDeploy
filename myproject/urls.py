"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login',views.login),
    path('api/logout',views.logout),
    path('api/signup',views.signup),
    path('api/changepassword',views.changePassword),
    path('api/propertydetails',views.propertydetails),
    path('api/search',views.searchdetails),
    path('api/profilepicture',views.profilepicture),
    path('api/rent',views.rent),
    path('api/readytomove',views.readytomove),
    path('api/underconstruction',views.underconstruction),
    path('api/accountdetails',views.accountdetails)
    
]
urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


