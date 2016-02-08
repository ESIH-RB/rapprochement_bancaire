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

def getValidLineSOGEBANK(sheet):
    fil = []
    for line in range(sheet.nrows):
            row = sheet.row_values(line)
            # print(row)
            #6,7,9,13,14 important Lines in SOGEBANK's sheet
            if line > 11: 
                if not ((row[6] == '') and (row[7] == '') and (row[9] == '') and (row[13] == '') and (row[15] == '')):
                    # print(row[6]+"|"+row[7]+"|"+row[9]+"|"+row[13]+"|"+row[15]+"<br />")
                    tmp = [row[6],row[7],row[9],row[13],row[15]]
                    fil.append(tmp)
    return fil

def putInLineSOGEBANK(tab): #Put in line SOGEBANK's file important infomations
    final = []
    for i in range(len(tab)):
        if i > 0:
            if tab[i][3] == '':
                sov = tab[i]
            else:
                sov[3]=tab[i][3]
                final.append(sov)
    return final

def handle_SOGEBANK(sheet):
    return putInLineSOGEBANK(getValidLineSOGEBANK(sheet))


def excel_handle(request):
    
    if request.method == 'POST':
        file_path = os.path.join(APP_DIR, 'files/my.xls')
        print(request.FILES)
        uploadFile(request.FILES['file2'],"a.xls")
        uploadFile(request.FILES['fichier'],"b.xls")
        egalite = [] #contient les lignes avec les informations d'egalite
        inegalite = [] # contient les lignes avec les information d'inegalite

        adr1 = os.path.join(APP_DIR, 'files/a.xls')
        adr2 = os.path.join(APP_DIR, 'files/b.xls')

        qb = xlrd.open_workbook(adr1)
        so = xlrd.open_workbook(adr2)
        #print(wb.sheet_names())
        qbI = qb.sheet_by_index(0)
        soI = so.sheet_by_index(0)


        
        final = handle_SOGEBANK(qbI)
        for j in range(len(final)):
            print(final[j])


        # for line in range(qbI.nrows):
        #     print(qbI.row_values(line))


        # print("Apres Quickbooks")
        
        # for line in range(soI.nrows):
        #     print(soI.row_values(line))
        # for t in range(sh.nrows):
        #     if t > 5:
        #         #print(sh.row_values(t))
        #         ll = sh.row_values(t)
        #         dict = {'Transaction':ll[2],'Amount': ll[9]}
        #         rlst.append(dict)
        # sh2 = wb.sheet_by_index(1)

        # for t in range(sh2.nrows):
        #     if t > 5:
        #         print(sh2.row_values(t)[14])
        #         # ll2 = sh2.row_values(t)
        #         # dict = {'Transaction':ll2[2],'Amount': ll2[9]}
        #         # rlst2.append(dict)
        # return JsonResponse({'la':rlst})
        return HttpResponse("sUCCES")
    form = FichierForm()
    return render(request,'upload.html',{'form':form})

