from django.conf.urls import url, patterns
from django.contrib import admin      
from rapp import views

urlpatterns = patterns('',
	url(r'^comp/', views.excel_handle),
	url(r'^dash/', views.main),
	url(r'^createrapp/', views.createRapp),
	url(r'^dashboard/', views.dashboard),
	url(r'^showrapp/', views.showTables),
)
