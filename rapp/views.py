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

def uploadFile(f,name="fich.xls"):
    with open(APP_DIR+"/files/"+name,'wb+') as des:
        for chunk in f.chunks():
            des.write(chunk)


def excel_handle(request):
    
    if request.method == 'POST':
        file_path = os.path.join(APP_DIR, 'files/my.xls')
        uploadFile(request.FILES['file'],"my.xls")
        rlst = []
        rlst2 = []
        wb = xlrd.open_workbook(file_path)
        print(wb.sheet_names())
        sh = wb.sheet_by_index(0)
        for t in range(sh.nrows):
            if t > 5:
                #print(sh.row_values(t))
                ll = sh.row_values(t)
                dict = {'Transaction':ll[2],'Amount': ll[9]}
                rlst.append(dict)
        sh2 = wb.sheet_by_index(1)

        for t in range(sh2.nrows):
            if t > 5:
                print(sh2.row_values(t)[14])
                # ll2 = sh2.row_values(t)
                # dict = {'Transaction':ll2[2],'Amount': ll2[9]}
                # rlst2.append(dict)
        return JsonResponse({'la':rlst})
    form = FichierForm()
    return render(request,'upload.html',{'form':form})

