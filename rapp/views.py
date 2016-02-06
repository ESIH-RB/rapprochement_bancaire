from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
# Create your views here.
from rapp.forms import FichierForm
import django_excel as excel
import xlrd
import os
#import pyexcel.ext.xls 
#import pyexcel.ext.xlsx 

APP_DIR = os.path.dirname(__file__)  # get current directory
#file_path = os.path.join(APP_DIR, 'baz.txt')  || File path to use in searching uploaded's file

def parse(request, data_struct_type):
    form = FichierForm(request.POST, request.FILES)
    if form.is_valid():
        filehandle = request.FILES['file']
        if data_struct_type == "array":
            return JsonResponse({"result": filehandle.get_array()})
        elif data_struct_type == "dict":
            return JsonResponse(filehandle.get_dict())
        elif data_struct_type == "records":
            return JsonResponse({"result": filehandle.get_records()})
        elif data_struct_type == "book":
            return JsonResponse(filehandle.get_book().to_dict())
        elif data_struct_type == "book_dict":
            return JsonResponse(filehandle.get_book_dict())
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


def excel_handle(request):
    
    if request.method == 'POST':
        file_path = os.path.join(APP_DIR, 'files/namesdemo.xls')
        wb = xlrd.open_workbook(file_path)
        #print(wb.sheet_names())
        sh = wb.sheet_by_index(3)
        for t in range(sh.nrows):
            print(sh.row_values(t))
    form = FichierForm()
    return render(request,'upload.html',{'form':form})

