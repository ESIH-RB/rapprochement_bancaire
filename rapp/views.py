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

#SOGEBANK's method for operations
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
    #Removing '-' sign preventing convertion to fload
    for z in range(len(final)):
        if final[z][3] == '-':
            final[z][3] = '0'
        if final[z][4] == '-':
            final[z][4] = '0'
    #Removing '-' sign preventing convertion to fload
    return final

def handle_SOGEBANK(sheet):
    return putInLineSOGEBANK(getValidLineSOGEBANK(sheet))
#SOGEBANK's method for operations

#Quickbooks version test handling
def handle_QuickBooksv1(sheet):
    all = []
    for z in range(sheet.nrows):
            if z > 4:
                all.append(sheet.row_values(z))
    return all
#Quickbooks version test handling


#Comparaison
def convertingTOFloat(values):
    try:
        v = float(values)
        return v
    except:
        r1 = values.replace(" ","")
        r2 = r1.replace(",",".")
        return float(r2)
def comparingFiles(quickBv1,sogebank):
    Cmp = []
    for i in range(len(quickBv1)):#QuickBooks
            for j in range(len(sogebank)):#SOGEBANK
                if quickBv1[i][2] == 'Expense':
                    if (convertingTOFloat(quickBv1[i][9])*-1) == convertingTOFloat(sogebank[j][3]):
                        dict = {'Transaction':quickBv1[i][2],'Posting':quickBv1[i][4],'Name':quickBv1[i][5],'Split':quickBv1[i][8],'Amount':quickBv1[i][9],'Date Eff':sogebank[j][0],'Cheque':sogebank[j][1],'Description':sogebank[j][2],'Debit':sogebank[j][3],'Credit':sogebank[j][4]}
                        Cmp.append(dict)
                        # print(str(quickBv1[i][2])+" "+str(quickBv1[i][4])+" "+str(quickBv1[i][5])+" "+str(quickBv1[i][8])+" "+str(quickBv1[i][9])+" "+str(sogebank[j][0])+" "+str(sogebank[j][1])+" "+str(sogebank[j][2])+" "+str(sogebank[j][3])+" "+str(sogebank[j][4]))
    return Cmp
#Comparaison
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


        
        soge = handle_SOGEBANK(qbI)
        qq = handle_QuickBooksv1(soI)
        
        # print("Soge"+ str(len(final1)))
        # print("Quickbooks"+ str(len(final)))
        # for zz in range(len(final1)):
        #     print(final1[zz])

        
        #Handling Comparaison
        # for i in range(len(final)):#QuickBooks
        #     for j in range(len(final1)):#SOGEBANK
        #         if final[i][2] == 'Expense':
        #             if (convertingTOFloat(final[i][9])*-1) == convertingTOFloat(final1[j][3]):
        #                 print(str(final[i][2])+" "+str(final[i][4])+" "+str(final[i][5])+" "+str(final[i][8])+" "+str(final[i][9])+" "+str(final1[j][0])+" "+str(final1[j][1])+" "+str(final1[j][2])+" "+str(final1[j][3])+" "+str(final1[j][4]))

                        # print("OK"+str(convertingTOFloat(final[i][9])*-1)+str(convertingTOFloat(final1[j][3])))
                        # print(final[i][5]+final[i][6])
        #Handling Comparaison

        #print(comparingFiles(qq,soge))
        return JsonResponse({'comp':comparingFiles(qq,soge)})
    form = FichierForm()
    return render(request,'upload.html',{'form':form})

