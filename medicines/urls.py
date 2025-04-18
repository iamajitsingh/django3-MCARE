"""medicines URL Configuration

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
from search import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # Prescribe Medicines Section
    path('search', views.search, name='search'),
    path('result/', views.searchresult, name='searchresult'),
    path('allresult/', views.allresult, name='allresult'),

    # COVID-19 Help Section
    path('covid', views.covidhome, name='covidhome'),
    path('showrem', views.showrem, name='showrem'),
    path('vaccine', views.vaccine, name='vaccine'),
    path('tozi', views.tozi, name='tozi'),
    path('bloodamb', views.bloodamb, name='bloodamb'),

    #COVID-19 Forum Section
    path('display_help', views.display_help, name='display_help'),
    path('ask_help', views.ask_help, name='ask_help'),
    path('completed_help', views.completed_help, name='completed_help'),

    # About us
    path('about', views.about, name='about'),

]
