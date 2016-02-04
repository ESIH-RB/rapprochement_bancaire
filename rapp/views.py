from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rapp.forms import FichierForm
import django_excel as excel
def excel_handle(request):
	#return HttpResponse("alksdjf;aksdjfa")
	#fichier = request.FILES['fichier']
	#dd = fichier.get_dict()

	#print(dd)
	#return excel.make_response(fichier.get_sheet(),'xls')

	if request.method == 'POST':
		fichier = request.FILES['fichier']
		qwer = fichier.get_dict()
		print(qwer)

		return HttpResponse("<strong>Succes<strong>")

	form = FichierForm()
	return render(request,'upload.html',{"form":form})