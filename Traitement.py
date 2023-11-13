import math
import csv
import random
import sys


def nettoyer_texte(file):
	f = open(file, 'r')
	txt=f.read()
	
	res=""

	for i in txt:
		if ord(i.upper()) in range(65,98):
			res += i.upper()
	f.close()
	return res

def txt_to_dico(file):
	f = open(file, 'r')
	txt=f.read()
	f.close()
	return txt



def dico_to_csv(file,n):
	if (n<1 or n>5):
		print("Error : n doit être compris entre 1 et 5\n")
		exit()

	txt=txt_to_dico(file)

	dico={}

	for i in range(0, len(txt)-n):
		res=txt[i:i+n]

		if res in dico:
			dico[res]+=1
		else:
			dico[res]=1
	dico = dict(sorted(dico.items(), key=lambda x:x[1]))
	name_f=str(n)+"-gram.csv"

	with open(name_f, 'w') as f:
		for key in dico.keys():
			f.write("%s,%s\n"%(key,dico[key]))

def csv_to_dico(fich_csv):

	# Initialiser le dictionnaire
	dico = {}
	csv.field_size_limit(sys.maxsize)
	# Ouvrir le fichier CSV en mode lecture
	with open(fich_csv, 'r') as fichier_csv:
		lecteur_csv = list(csv.reader(fichier_csv))

		for ligne in lecteur_csv:
			index = ligne[0]  
			valeur = int(ligne[1])
			dico[index] = valeur

	# Afficher le dictionnaire résultant

	return dico






