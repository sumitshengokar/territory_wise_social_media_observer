from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('search/',views.search,name='search'),
    path('trends/',views.trends, name ='ggg'),
    path('show/',views.show,name='show'),
    path('top_trends/',views.top_trends,name='ttrr'),
    path('visualize/',views.visualize,name='vu'),
    path('hash/',views.hash,name='hash'),
    path('mentions/',views.mentions,name='mention'),
    path('location/',views.locat,name='location'),
    path('timeline/',views.timeline,name='time'),
    path('top_time/',views.top_time,name='top')

]