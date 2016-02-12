from django.db import models
from django.contrib.auth.models import User #Help in using Django's provided model to handle users credantials

# Create your models here.

class linkSOGEBANK(models.Model):
	name = models.CharField("Nom du fichier SOGEBANK telecharge",max_length=30,unique=True)
	added_Date = models.DateTimeField(auto_now=True)

class linqQUICKBOOKS(models.Model):
	name = models.CharField("Nom du fichier QUICKBOOKS telecharge",max_length=30,unique=True)
	added_Date = models.DateTimeField(auto_now=True)

class comparaison(models.Model):
	nomComparaison = models.CharField(max_length=40)
	cf_link_SOGEBANK = models.ForeignKey(linkSOGEBANK,on_delete=models.CASCADE,
		verbose_name="Reference du fichier SOGEBANK",)
	cf_link_QUICKBOOKS = models.ForeignKey(linqQUICKBOOKS,on_delete=models.CASCADE,
		verbose_name="Reference du fichier QUICKBOOKS",)
	own_by = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Proprietaire de la comparaison")
	ended = models.IntegerField("Si la comparaison a ete valide")
	dateValidate = models.DateTimeField(null=True) #date marquant la fin de la comparaison

class contenuSOGEBANK(models.Model):
	date = models.DateField()
	no_cheque = models.CharField("No du Cheque", max_length=30)
	description = models.TextField("Description")
	debit = models.FloatField("Montant en decimal du debit")
	crebit = models.FloatField("Montant en decimal du crebit")
	solde = models.FloatField("Montant en decimal du crebit")

class contenuQUICKBOOKS(models.Model):
	date = models.DateField()
	type_transaction = models.CharField(max_length=40)
	name = models.CharField(max_length=40)
	num = models.CharField(max_length=40)
	posting = models.CharField(max_length=40)
	memo = models.CharField(max_length=40)
	account = models.CharField(max_length=40)
	split = models.CharField(max_length=40)
	montant = models.FloatField("Montant en decimal du fichier QUICKBOOKS")


class validation(models.Model):
	comp = models.ForeignKey(comparaison,on_delete=models.CASCADE,verbose_name="Reference vers la comparaison")
	row_sogebank = models.ForeignKey(contenuSOGEBANK,on_delete=models.CASCADE,verbose_name="Reference vers la ligne d'un fichie SOGEBANK")
	row_quickbooks = models.ForeignKey(contenuQUICKBOOKS,on_delete=models.CASCADE,verbose_name="Reference vers la ligne d'un fichieR QUICKBOOKS")
	state = models.IntegerField("Etat de la validation")