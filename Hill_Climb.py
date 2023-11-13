import math
import csv
import random
import os
import sys
import matplotlib.pyplot as plt
from Traitement import *
import time

alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

MAX_GRAM=5

def dico_ngram(txt,n):
	"""
		return dictionnary with frequence of n-gram of txt as value 
		and n-gram as key
	"""

	if (n<1 or n>MAX_GRAM):
		print("Usage : n doit être compris entre 1 et 4\n")
		exit()

	dico={}

	for i in range(0, len(txt)-n):
		res=txt[i:i+n]

		if res in dico:
			dico[res]+=1
		else:
			dico[res]=1
	dico = dict(sorted(dico.items(), key=lambda x:x[1]))

	return dico


def decrypt(cipher,key):
	"""
		return decryption with key of cipher
	"""

	res=""

	for l in cipher :
	
		res+=chr(key.index(l)+65)
        
	return res


def getfitness(key,cipher,dict_ngram,n):
	"""	
		return score of cipher
	"""
	res=0

	uncipher=decrypt(cipher,key)

	for i in range (0,len(cipher)-n):
		st=uncipher[i:i+n]

		el=dict_ngram.get(st)


		if (el != None):
			
			res += math.log2(el)
		else:
			res += 0.0001

	return res

def getfitness_pearson(key,cipher,dict_ngram,n):
	"""
		return score of Pearson between dictionnary of n-gram of cipher and dict_ngram
	"""

	res=0

	uncipher=decrypt(cipher,key)
	dico1 = dict(sorted((dico_ngram(uncipher,n)).items(), key=lambda x:x[0]))
	dico2 = dict(sorted(dict_ngram.items(), key=lambda x:x[0]))

	# tres couteux
	dico1,dico2=sort_dico_pearson(dico1,dico2)

	L1=list(dico1.values())
	L2=list(dico2.values())

	haut=0
	basy=0
	basx=0

	if (sum(L1)==len(L1)):
		esper_x=(sum(L1)+1)*(1/len(L1))
	else:
		esper_x=sum(L1)*(1/len(L1))

	if (sum(L2)==len(L2)):
		esper_y=(sum(L2)+1)*(1/len(L2))
	else:
		esper_y=sum(L2)*(1/len(L2))


	for i in range (0,len(L1)):

		calcul_x=(L1[i]-esper_x)

		calcul_y=(L2[i]-esper_y)

		haut+=calcul_x*calcul_y
		basx+=calcul_x**2
		basy+=calcul_y**2

	
	res=round(haut/(math.sqrt(basx)*math.sqrt(basy)),5)

	return res

def sort_dico_pearson(dico1,dico2):
	"""
		sort alphabetically dico1 and dico2 and make intersection
	"""

	while (len(dico1)!=len(dico2)):
		if (len(dico1)<len(dico2)):
			dico2_copy=dico2.copy()
			for i in dico2:
				if i not in dico1:
					dico2_copy.pop(i)
			dico2=dico2_copy

		else:
			dico1_copy=dico1.copy()
			for i in dico1:
				if i not in dico2:
					dico1_copy.pop(i)
			dico1=dico1_copy

	return dico1,dico2


def gen_key():
	"""
		generation of random key
	"""

	res=""
	l=0
	for i in range(0,26):
		l+=1
		m=alphabet[random.randint(0,25)]
		while m in res:
			m=alphabet[random.randint(0,25)]
		res+=m
	return res


def gen_key2(key):
	"""
		generation of child key of key
	"""

	index1=random.randint(0,25)
	index2=random.randint(0,25)

	while (index1 == index2):
		index2=random.randint(0,25)

	k=list(key)
	tmp=k[index1]
	k[index1]=k[index2]
	k[index2]=tmp

	return "".join(k)


def nombre_caracteres_differents(chaine1, chaine2):
	"""
		return number of carac different between chaine1 and chaine2
	"""

	if len(chaine1) != len(chaine2):
		raise ValueError("Les chaînes doivent avoir la même longueur.")
    
	diff_count = 0
	for i in range(len(chaine1)):
		if chaine1[i] != chaine2[i]:
			diff_count += 1
    
	return diff_count


def hill_climbing(cipher,limited_step_local,fitness,dict_ngram,n,key_original):
	"""
		Return best key evaluated by fitness function with 
		limited_step loop turn without new best key
	"""

	# initialisation
	best=gen_key()
	best_fit=fitness(best,cipher,dict_ngram,n)
	step=0
	cpt=0
	l_score=[]
	l_iteration=[]

	seconds = time.time()

	while True:

		cpt+=1
		step+=1

		# generate new random key
		new_key=gen_key2(best)

		# evaluate with fitness function
		fit_new_key=fitness(new_key,cipher,dict_ngram,n)


		if fit_new_key>best_fit:
			
			# better key replace old key

			best_fit=fit_new_key
			best=new_key
			step=0
		l_score.append(best_fit)
		l_iteration.append(cpt)

		if (step==limited_step_local):
			break

	secondss = time.time()

	return best,best_fit,secondss-seconds,rate_decipher(cipher,key_original,best)



def rate_decipher(cipher,key_original,key_try):
	"""
		return rate of different charactere between 
		decipher with original key and decipher with
		best key found between 0 and 1 
	"""

	decipher_ori=decrypt(cipher,key_original)
	decipher_try=decrypt(cipher,key_try)

	return 1 - nombre_caracteres_differents(decipher_ori,decipher_try) / len(decipher_try)
	

def hill_climbing_itere(directory_txt,directory_key,nb_occu_limite,fitness,dict_ngram,n,nb_iter):
	"""
		Hill-Climbing with iterate on differents texts and key
		for make stats
	"""

	# initialisation
	succes=0
	echec=0
	rate_average=0
	len_smaller_txt=math.inf
	cpt=0

	# sort of file of key and cipher
	fichiers_tries_t = sorted(os.listdir(directory_txt), key=lambda x: x.lower())
	fichiers_tries_k = sorted(os.listdir(directory_key), key=lambda x: x.lower())
	fichiers_tries_t.remove(".DS_Store")


	for filename_txt,filename_key in zip(fichiers_tries_t,fichiers_tries_k):
		cpt+=1

		if (cpt==nb_iter):
			break

		f_txt=os.path.join(directory_txt,filename_txt)
		f_key=os.path.join(directory_key,filename_key)


		txt=nettoyer_texte(f_txt)
		original_key=nettoyer_texte(f_key)

		test_key,score,time,rate=hill_climbing(txt,nb_occu_limite,fitness,dict_ngram,n,original_key)
		rate_average+=rate_decipher(txt,original_key,test_key)

	return rate_average / nb_iter


def stat_csv(file_cipher,fitness,dict_ngram,n,key_original,file_direction):
	"""
		write in csv file statistiques of return of hill_climbing 
		with different value of limited_step
	"""

	header=["step","score","time",'decipher rate']
	print("step        score            time                  rate")
	f = open(file_cipher, 'r')
	cipher=f.read()
	f.close()

	with open(file_direction, 'w', encoding='UTF8') as f:
		writer = csv.writer(f)
		writer.writerow(header)

		for i in range (500, 2250,250):

			key,score,time,rate=hill_climbing(cipher,i,fitness,dict_ngram,n,key_original)
			print(i," ",score," ",time," ",rate)
			data=[i,round(score,3),round(time,2),round(rate,2)]
			writer.writerow(data)


def stat_txt(directory_txt,directory_key,nb_occu_limite,fitness,nb_iter):
	"""
		write statistics of succes or echec to have perfect key with hill_climbing on texts
		given as parameters
	"""

	# Données
	ngram=[]
	rate=[]

	for i in range(1, MAX_GRAM+1):
		gram=str(i)+"-gram"
		dico=csv_to_dico("Dico/"+gram+".csv")
	
		rate.append(hill_climbing_itere(directory_txt,directory_key,nb_occu_limite,fitness,dico,i,nb_iter))
		ngram.append(gram)
	

	# Création du graphique à barres
	plt.bar(ngram,rate)

	# Définition des limites de l'axe y
	plt.ylim(0, 1)

	# Ajout des étiquettes sur les axes
	plt.xlabel("Mesures")
	plt.ylabel("Note")

	# Affichage du graphique
	plt.show()


if __name__ == "__main__":

	print("1 - create new dico in csv file\n2 - create stats with folder of cipher and keys\n3 - create stats with different values of local iterations")

	ch = input()

	
	match int(ch) :

		case 1 :
			print("dico file directory ?\n")
			dico=input()
			print("n-gram ?\n")
			n=input()
			dico_to_csv(dico,int(n))

		case 2:
			print("cipher folder directory ?\n")
			chiffr=input()
			print("key folder directory ?\n")
			key=input()
			print("number of step limit ?\n")
			step=input()
			print("number of text analysis ?\n")
			cpt=input()
			stat_txt(chiffr,key,int(step),getfitness,int(cpt))

		case 3:
			print("cipher file ?\n")
			chiffr=input()
			print("Dico directory ?\n")
			dico=input()
			print("ngram ?\n")
			n=input()
			print("key ?\n")
			key=input()
			print("file direction ?\n")
			file=input()
			stat_csv(chiffr,getfitness,csv_to_dico(dico),int(n),key,file)






