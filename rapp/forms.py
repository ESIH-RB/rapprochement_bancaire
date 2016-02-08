from django import forms

class FichierForm(forms.Form):
	nom = forms.CharField(help_text="Specifier le nom du fichier")
	fichier = forms.FileField(help_text="Le fichier1")
	file2 = forms.FileField(help_text="Le fichier2")