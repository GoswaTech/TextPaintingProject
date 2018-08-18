#!/usr/bin/python

import os
import glob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as smisc
from math import sqrt

def VMin(tab):
	tmp = 255
	for eachRaw in tab:
		for eachPix in eachRaw:
			if(eachPix[0] < tmp):
				tmp = eachPix[0]
			if(eachPix[1] < tmp):
				tmp = eachPix[1]
			if(eachPix[2] < tmp):
				tmp = eachPix[2]
	return tmp

def VMax(tab):
	tmp = 0
	for eachRaw in tab:
		for eachPix in eachRaw:
			if(eachPix[0] > tmp):
				tmp = eachPix[0]
			if(eachPix[1] > tmp):
				tmp = eachPix[1]
			if(eachPix[2] > tmp):
				tmp = eachPix[2]
	return tmp

def searchIMax(tab):
	ret = 0
	cur = 0
	for element in tab:
		if(element > ret):
			ret = cur
			cur = cur + 1
	return ret

def NoirEtBlanc(imgAr):
	for eachRow in imgAr:
		for eachPix in eachRow:
			moy = (eachPix[0] + eachPix[1] + eachPix[2])/3
			eachPix[0] = moy
			eachPix[1] = moy
			eachPix[2] = moy
	
	return imgAr

def colorIt(curseur, text, lettre):
	try:
		return ord(text[(curseur*3)+lettre])
	except:
		return 0

def CreerImage(text, version, showImage, verbose):
	if(version == 1 ):
		print('[INFO] Methode 1 chosie')
		return CreationImage(text, showImage, verbose)
	elif(version == 2):
		print('[INFO] Methode 2 choisie')
		return CreationImage2(text, showImage, verbose)

def CreationImage(text, showImage, verbose):
	print('[INFO] Image en Creation')
	curseur = 0
	dim = len(text)/3
	newAr = np.array(Image.new('RGB', (int(sqrt(dim)), int(sqrt(dim)))))
	print('[INFO] Dimensions image : ' + str(dim))
	for eachRow in newAr:
		for eachPix in eachRow:
			premiereLettre = colorIt(curseur, text, 0)
			deuxiemeLettre = colorIt(curseur, text, 1)
			troisiemeLettre = colorIt(curseur, text, 2)
			eachPix[0] = premiereLettre
			eachPix[1] = deuxiemeLettre
			eachPix[2] = troisiemeLettre
			curseur = curseur + 1
			if(verbose):
				print('Pix : ' + str(curseur) + str(eachPix))
				print('\t- Red : ' + str(eachPix[0]))
				print('\t- Green : ' + str(eachPix[1]))
				print('\t- Blue : ' + str(eachPix[2]))
	if(showImage):
		plt.imshow(newAr)
		plt.show()
	return newAr

def CreationImage2(text, showImage, verbose):
	print('[INFO] Image2 en Creation')
	curseur = 0
	curseur = 0
	dim = len(text)/3
	newAr = np.array(Image.new('RGB', (dim, dim)))
	print('[INFO] Dimensions image : ' + str(dim))
	for eachRow in newAr:
		premiereLettre = colorIt(curseur, text, 0)
		deuxiemeLettre = colorIt(curseur, text, 1)
		troisiemeLettre = colorIt(curseur, text, 2)
		if(verbose):
			print('Row : ' + str(curseur))
			print('\t- Red : ' + str(premiereLettre) + ' (' + chr(premiereLettre) + ')')
			print('\t- Green : ' + str(deuxiemeLettre) + ' (' + chr(deuxiemeLettre) + ')')
			print('\t- Blue : ' + str(troisiemeLettre) + ' (' + chr(troisiemeLettre) + ')')
		for eachPix in eachRow:
			eachPix[0] = premiereLettre
			eachPix[1] = deuxiemeLettre
			eachPix[2] = troisiemeLettre
		curseur = curseur + 1
	if(showImage):
		plt.imshow(newAr)
		plt.show()
	return newAr

def Methode1(tableau, pathToBackImage, showImage, verbose):
	print('[INFO] Methode 1')
	img = Image.open(pathToBackImage)
	imgAr = np.array(smisc.imresize(img.copy(), (len(tableau[0]),len(tableau))))
	print('[INFO] BackImage en cache et redimonsionne')
	diviseur = input('Saisir N (Intensite/N) : ')
	indexRow = 0
	indexPix = 0
	
	for eachRow in imgAr:
		for eachPix in eachRow:
			moy = (eachPix[0] + eachPix[1] + eachPix[2])/3
			eachPix[0] = moy
			eachPix[1] = moy
			eachPix[2] = moy
			
			if(verbose):
				print('Moy : ' + str(moy))
	
	if(showImage):
		plt.imshow(imgAr)
		plt.show()
	
	for eachRow in tableau:
		indexPix = 0
		for eachPix in eachRow:
			modif = imgAr[indexRow][indexPix][0]/diviseur
			iMax = searchIMax(eachPix)
			eachPix[iMax] = int(eachPix[iMax] + modif)
			
			if(verbose):
				print('[INFO] Row : ' + str(indexRow) + 'Pix : ' + str(indexPix))
				print('\t- red : ' + str(eachPix[0]))
				print('\t- green : ' + str(eachPix[1]))
				print('\t- blue : ' + str(eachPix[2]))
			
			indexPix = indexPix + 1
		indexRow = indexRow + 1
	
	if(showImage):
		plt.imshow(tableau)
		plt.show()
	
	return tableau

def Methode2(tableau, pathToBackImage, showImage, verbose):
	print('[INFO] Methode 2')
	img = Image.open(pathToBackImage)
	imgAr = np.array(smisc.imresize(img.copy(), (len(tableau[0]),len(tableau))))
	print('[INFO] BackImage en cache et redimonsionne')
	red = float(input('Pourcentage de rouge : '))/100
	green = float(input('Pourcentage de vert : '))/100
	blue = float(input('Pourcentage de bleu : '))/100
	addition = input('Addition (1) | Soustraction (0) : ')
	indexRow = 0
	indexPix = 0
	
	imgAr = NoirEtBlanc(imgAr)
	
	if(showImage):
		plt.imshow(imgAr)
		plt.show()
	
	for eachRow in tableau:
		indexPix = 0
		for eachPix in eachRow:
			modif = imgAr[indexRow][indexPix][0]
			if(addition):
				eachPix[0] = int(eachPix[0] + float(modif)*red)
				eachPix[1] = int(eachPix[1] + float(modif)*green)
				eachPix[2] = int(eachPix[2] + float(modif)*blue)
			else:
				eachPix[0] = int(eachPix[0] - float(modif)*red)
				eachPix[1] = int(eachPix[1] - float(modif)*green)
				eachPix[2] = int(eachPix[2] - float(modif)*blue)
			
			if(verbose):
				print('[INFO] Row : ' + str(indexRow) + 'Pix : ' + str(indexPix))
				print('\t- red : ' + str(eachPix[0]))
				print('\t- green : ' + str(eachPix[1]))
				print('\t- blue : ' + str(eachPix[2]))
			
			indexPix = indexPix + 1
		indexRow = indexRow + 1
	
	if(showImage):
		plt.imshow(tableau)
		plt.show()
	
	return tableau

def FocusColors(tableau, showImage, verbose):
	min = float(VMin(tableau))
	max = float(VMax(tableau))
	print('[INFO] Min : ' + str(int(min)) + ' Max : ' + str(int(max)))
	if(verbose):
		for eachRow in tableau:
			for eachPix in eachRow:
				print('\t- red : ' + str(eachPix[0]))
				eachPix[0] = int((float(eachPix[0])-min)/(max-min)*255)
				print('\t-> - red : ' + str(eachPix[0]))
				print('\t- green : ' + str(eachPix[1]))
				eachPix[1] = int((float(eachPix[1])-min)/(max-min)*255)
				print('\t-> - green : ' + str(eachPix[1]))
				print('\t- blue : ' + str(eachPix[2]))
				eachPix[2] = int((float(eachPix[2])-min)/(max-min)*255)
				print('\t-> - blue : ' + str(eachPix[2]))
	else:
		for eachRow in tableau:
			for eachPix in eachRow:
				eachPix[0] = int((float(eachPix[0])-min)/(max-min)*255)
				eachPix[1] = int((float(eachPix[1])-min)/(max-min)*255)
				eachPix[2] = int((float(eachPix[2])-min)/(max-min)*255)
	if(showImage):
		plt.imshow(tableau)
		plt.show()
	
	return tableau

def TraitementImage(tableau, pathToBackImage, version, showImage, verbose):
	if(version == 0):
		return tableau
	if(version == 1):
		Methode1(tableau, pathToBackImage, showImage, verbose)
	if(version == 2):
		Methode2(tableau, pathToBackImage, showImage, verbose)
	
	return tableau

def SaveImage(nomImage, tableau):
	newimage = Image.new('RGB', (len(tableau[0]), len(tableau)))
	newimage.putdata([tuple(p) for row in tableau for p in row])
	newimage.save(nomImage)
	print('[INFO] Image Sauvee')

def LoadBackImage(absPath):
	liste = glob.glob(absPath + "/res/backimage.*")
	for files in liste:
		extension = files.split('backimage.')[1]
		if(extension == 'jpg'):
			print('[INFO] Extension : jpg\nConversion en png')
			#ConvertJPGToPNG(files)
		elif(extension == 'png'):
			print('[INFO] Extension : png')

def main():
	##### Initiation de l'environnement de travail
	absPath = os.path.abspath('.')
	try:
		os.mkdir(absPath + '/img')
		print('[INFO] Dossier img cree')
	except:
		print('[INFO] Dossier img existant')
	
	##### Mise en memoire des variables
	print('[INFO] Programme Lance')
	text = open('res/textAPeindre.txt').read()
	print('[INFO] Text en cache')
	
	##### Recherche de l'image a importer
	LoadBackImage(absPath)
	pathToBackImage = absPath + '/res/backimage.png'
	
	##### Image
	
	# Creation
	tableau = CreerImage(text, 2, True, False)
	
	# Traitement
	tableau = FocusColors(tableau,  True, False)
	tableau = TraitementImage(tableau, pathToBackImage, input("Mode de traitement : "), True, False)
	
	# Save
	nomFichier = raw_input('[INFO] Exportation\nNom de l\'image : ')
	SaveImage('img/' + nomFichier + '.png', tableau)

main()