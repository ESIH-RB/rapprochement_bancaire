from django.conf.urls import url, patterns
from django.contrib import admin      
from rapp import views

urlpatterns = patterns('',
	url(r'^comp/', views.excel_handle),
	url(r'^dash/', views.main)
)
