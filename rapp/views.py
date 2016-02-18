from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
# Create your views here.
from rapp.forms import FichierForm
import xlrd
import os
import random
from rapp.models import *
from django.contrib.auth.models import User
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
    InCmp = []
    for i in range(len(quickBv1)):#QuickBooks
            for j in range(len(sogebank)):#SOGEBANK
                if quickBv1[i][2] == 'Expense':
                    if (convertingTOFloat(quickBv1[i][9])*-1) == convertingTOFloat(sogebank[j][3]):
                        dict = {'Transaction':quickBv1[i][2],'Posting':quickBv1[i][4],'Name':quickBv1[i][5],'Split':quickBv1[i][8],'Amount':quickBv1[i][9],'Date Eff':sogebank[j][0],'Cheque':sogebank[j][1],'Description':sogebank[j][2],'Debit':sogebank[j][3],'Credit':sogebank[j][4]}
                        Cmp.append(dict)
                        # print(str(quickBv1[i][2])+" "+str(quickBv1[i][4])+" "+str(quickBv1[i][5])+" "+str(quickBv1[i][8])+" "+str(quickBv1[i][9])+" "+str(sogebank[j][0])+" "+str(sogebank[j][1])+" "+str(sogebank[j][2])+" "+str(sogebank[j][3])+" "+str(sogebank[j][4]))
                    else:
                        dict2 = {'Transaction':quickBv1[i][2],'Posting':quickBv1[i][4],'Name':quickBv1[i][5],'Split':quickBv1[i][8],'Amount':quickBv1[i][9],'Date Eff':sogebank[j][0],'Cheque':sogebank[j][1],'Description':sogebank[j][2],'Debit':sogebank[j][3],'Credit':sogebank[j][4]}
                        InCmp.append(dict2)
    rslt = []
    rslt.append({'cmp':Cmp,'incmp':InCmp})
    return rslt
#Comparaison

#NamesFilesFUnnctions
def namesFiles(filename):
    chif = [1,2,3,4,5,6,7,8,9,0]
    lettr = ['a','A','b','B','c','C','d','D','e','E']
    chaine = ""
    for i in range(6):
        chx = random.randrange(0,9,3)
        chaine+= str(chif[chx])
        chaine+= str(lettr[(chx+3)%10])
    r = filename.split('.',1)

    nomFile = chaine+"."+r[1]

    return nomFile
#NamesFilesFUnnctions
def excel_handle(request):
    if request.method == 'POST':
        # print(request.POST['cmpname'])
        vldNameSog = namesFiles(str(request.FILES['soge']))
        vldNameQuick = namesFiles(str(request.FILES['quick']))
        
        uploadFile(request.FILES['soge'],vldNameSog)#uploadSogeFiles
        uploadFile(request.FILES['quick'],vldNameQuick)#uploadQuickBooks

        sogB = linkSOGEBANK(name = vldNameSog)
        sogB.save()
        quickB = linqQUICKBOOKS(name = vldNameQuick)
        quickB.save()

        c = linkSOGEBANK.objects.get(name= vldNameSog)
        b = linqQUICKBOOKS.objects.get(name= vldNameQuick)

        #getConnectedUser
        user = User.objects.get(username="admin")
        #getConnectedUser

        #CreateLink for comparaison between files
        compC = comparaison(nomComparaison = request.POST['cmpname'],cf_link_SOGEBANK=c, cf_link_QUICKBOOKS=b,ended=0,own_by = user)
        compC.save()

        #CreateLink for comparaison between files

        
        # print(quickB)
        return HttpResponse("<strong>Telechargement du fichier reussi retourne au <a href='/excel/dashboard/'>Dashboard</a></strong>")
    else:
        return render(request,'app/crapp.html',{})


def main(request):
    return render(request,'app/test.html')

def createRapp(request):
    return render(request,'app/crapp.html',{})

def dashboard(request):
    return render(request,'app/dashboard.html',{})

def showTables(request):
    compp = comparaison.objects.all()
    for ass in compp:
        print(ass.nomComparaison+" "+str(ass.id))
    return render(request,'app/showAll.html',{'all':compp})

def descripComp(request,indice):
    comp = comparaison.objects.get(id = int(indice))
    sogeFile = comp.cf_link_SOGEBANK.name
    quickFile = comp.cf_link_QUICKBOOKS.name
    print(sogeFile+" "+quickFile)

    adr1 = os.path.join(APP_DIR, 'files/'+sogeFile)
    adr2 = os.path.join(APP_DIR, 'files/'+quickFile)

    so = xlrd.open_workbook(adr1)
    qb = xlrd.open_workbook(adr2)
    
    soI = so.sheet_by_index(0)
    qbI = qb.sheet_by_index(0)

    soge = handle_SOGEBANK(soI)
    qq = handle_QuickBooksv1(qbI)

    zz = comparingFiles(qq,soge)

    egal = zz[0]['cmp']
    inegal = zz[0]['incmp']
    return render(request,'app/show.html',{'ine':inegal,'equal':egal})
    # return JsonResponse({'ss':comparingFiles(qq,soge)})