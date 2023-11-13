import math
import csv
import random
import sys
import re

def nettoyer_texte(file):
	f = open(file, 'r')
	txt=f.read()
	
	res=""

	for i in txt:
		if ord(i.upper()) in range(65,98):
			res += i.upper()
	f.close()

	name_file=(re.search(r'^([^.]*)', file).group(1))+"_nettoye"
	fichier = open(name_file, "w")
	fichier.write(res)
	fichier.close()

if __name__ == "__main__":
	nettoyer_texte(sys.argv[1])