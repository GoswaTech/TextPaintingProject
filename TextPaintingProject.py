#!/usr/bin/python

# -*- coding: utf-8 -*-

import os
import glob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as smisc
from math import sqrt
import wave
import binascii

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

def colorLine(newAr, intensite, curseur):
	for eachPix in newAr[curseur/3]:
		eachPix[curseur%3] = intensite
	return newAr

def TextToVers(text):
	vers = text.split('\n')
	return vers

def FramesToHexa(frames, poids, verbose):
	print('[INFO] Frames to Hexa')
	ret = []
	tmp = ''
	cnt = 1
	for eachLettre in frames:
		if(cnt < poids*2):
			tmp = tmp + eachLettre
			cnt = cnt + 1
		else:
			ret.append(tmp + eachLettre)
			tmp = ''
			cnt = 1
	if(verbose):
		print('[VERBSOE] Taille : ' + str(len(ret)) + ' octets')
		print('\tApercu : ' + str(ret[1323000:1323050]))
	return ret

def SeparationCanaux(textHexa, verbose):
	print('[INFO] Separation Canaux')
	canalG = True
	textCanaux = [[],[]]
	for eachValue in textHexa:
		if(canalG):
			textCanaux[0].append(eachValue)
			canalG = False
		else:
			textCanaux[1].append(eachValue)
			canalG = True
	if(verbose):
		print('#####\n[VERBOSE] ' + str(len(textCanaux)) + ' Canaux')
		print(' Taille Canal Gauche : ' + str(len(textCanaux[0])) + ' Echantillons')
		print('\tApercu : ' + str(textCanaux[0][1323000/2:1323050/2]))
		print('Taille Canal Droit : ' + str(len(textCanaux[1])) + ' Echantillons')
		print('\tApercu : ' + str(textCanaux[1][1323000/2:1323050/2]))
	
	return textCanaux

def MoySecHex(textCanaux, frameRate, verbose):
	print('[INFO] Moyenne par seconde')
	somme = 0
	moy = [[],[]]
	for canal in range(2):
		print('Canal ' + str(canal))
		for i in range(len(textCanaux[canal])/frameRate):
			somme = 0
			for indexValue in range(frameRate):
				somme = somme + int(textCanaux[canal][i*frameRate + indexValue], 16)
			
			somme = somme/frameRate
			moy[canal].append(somme)
	
	if(verbose):
		print('#####\n[VERBOSE] Taille Canaux : G ' + str(len(moy[0])) + ' | D ' + str(len(moy[1])))
		print('\tApercu : ' + str(hex(moy[0][1323000/2/frameRate])))
	return moy

def CreerImage(text, version, showImage, verbose):
	if(version == 1 ):
		print('[INFO] Methode 1 chosie')
		return CreationImage(text, showImage, verbose)
	elif(version == 2):
		print('[INFO] Methode 2 choisie')
		return CreationImage2(text, showImage, verbose)
	elif(version == 3):
		print('[INFO] Methode 3 choisie')
		return CreationImage3(text, showImage, verbose)

def verifIntensity(eachPix):
	for eachColor in eachPix:
		if(eachColor > 255):
			eachColor = 255
		elif(eachColor < 0):
			eachColor = 0
	return eachPix

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
	dim = len(text)/3
	if(len(text)%3 != 0):
		dim = dim + 1
	
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

def CreationImage3(text, showImage, verbose):
	print('[INFO] Image3 en Creation')
	curseur = 0
	vers = TextToVers(text)
	dim = 0
	for i in vers:
		dim = dim + (len(i)/3)
		if(len(i)%3 != 0):
			dim = dim + 1
	
	newAr = np.array(Image.new('RGB', (dim, dim)))
	print('[INFO] Dimensions image : ' + str(dim))
	
	for eachVers in vers:
		for indexChar in range(len(eachVers)):
			newAr = colorLine(newAr, ord(eachVers[indexChar]), curseur)
			
			if(ord(eachVers[indexChar]) == 13):
				if(len(eachVers) != 0):
					if(len(eachVers)%3 == 1):
						newAr = colorLine(newAr, ord(eachVers[indexChar]), curseur)
						curseur = curseur + 1
						newAr = colorLine(newAr, ord(eachVers[indexChar]), curseur)
						curseur = curseur + 1
						newAr = colorLine(newAr, ord(eachVers[indexChar]), curseur)
					if(len(eachVers)%3 == 2):
						newAr = colorLine(newAr, ord(eachVers[indexChar]), curseur)
						curseur = curseur + 1
						newAr = colorLine(newAr, ord(eachVers[indexChar]), curseur)
			if(verbose):
					print('Row : ' + str(curseur/3) + ' \n\tColors : ' + str(curseur%3) + ' -> ' + str(ord(eachVers[indexChar])) + ' (' + str(eachVers[indexChar]) + ')')
			curseur = curseur + 1
	if(showImage):
		plt.imshow(newAr)
		plt.show()
	
	return newAr

def TraitementImage(tableau, pathToBackImage, version, showImage, verbose):
	if(version == 0):
		return tableau
	if(version == 1):
		Methode1(tableau, pathToBackImage, showImage, verbose)
	if(version == 2):
		Methode2(tableau, pathToBackImage, showImage, verbose)
	if(version == 3):
		Methode3(tableau, pathToBackImage, showImage, verbose)
	
	return tableau

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
				print('[VERSBOSE] Row : ' + str(indexRow) + ' Pix : ' + str(indexPix))
				print('\t- red : ' + str(eachPix[0]))
				print('\t- green : ' + str(eachPix[1]))
				print('\t- blue : ' + str(eachPix[2]))
			
			indexPix = indexPix + 1
		indexRow = indexRow + 1
	
	if(showImage):
		plt.imshow(tableau)
		plt.show()
	
	return tableau

def Methode3(tableau, pathToBackImage, showImage, verbose):
	print('[INFO] Methode 3')
	img = Image.open(pathToBackImage)
	imgAr = np.array(smisc.imresize(img.copy(), (len(tableau[0]),len(tableau))))
	print('[INFO] BackImage en cache et redimonsionne')
	if(input("Pourcentage Couleur pas Couleur ? yes(1) | no(0) ")):
		red = float(input('Pourcentage de rouge BackImage : '))/100
		green = float(input('Pourcentage de vert BackImage : '))/100
		blue = float(input('Pourcentage de bleu BackImage : '))/100
		redP = float(input('Pourcentage de rouge TextPainted : '))/100
		greenP = float(input('Pourcentage de vert TextPainted : '))/100
		blueP = float(input('Pourcentage de bleu TextPainted : '))/100
	else:
		pourcentageBackImage = input('Pourcentage de BackImage : ')
		pourcentageTextPainted = input('Pourcentage de TextPainted : ')
		red = float(pourcentageBackImage)/100
		green = float(pourcentageBackImage)/100
		blue = float(pourcentageBackImage)/100
		redP = float(pourcentageTextPainted)/100
		greenP = float(pourcentageTextPainted)/100
		blueP = float(pourcentageTextPainted)/100
	indexRow = 0
	indexPix = 0
	
	if(showImage):
		plt.imshow(imgAr)
		plt.show()
	
	for eachRow in tableau:
		indexPix = 0
		for eachPix in eachRow:		
			if(verbose):
				print('[VERBOSE] Row : ' + str(indexRow) + ' Pix : ' + str(indexPix))
				modif = imgAr[indexRow][indexPix]
				print('BackImage : ' + str(modif))
				
				print('\t- red : ' + str(eachPix[0]))
				eachPix[0] = int( (float(eachPix[0])*redP + float(modif[0])*red) )
				print('\t- red (new) : ' + str(eachPix[0]))
				
				print('\t- green : ' + str(eachPix[1]))
				eachPix[1] = int( (float(eachPix[1])*greenP + float(modif[1])*green) )
				print('\t- green (new) : ' + str(eachPix[1]))
				
				print('\t- blue : ' + str(eachPix[2]))
				eachPix[2] = int( (float(eachPix[2])*blueP + float(modif[2])*blue) )
				print('\t- blue (new) : ' + str(eachPix[2]))
			else:
				modif = imgAr[indexRow][indexPix]
				eachPix[0] = int( (float(eachPix[0])*redP + float(modif[0])*red) )
				eachPix[1] = int( (float(eachPix[1])*greenP + float(modif[1])*green) )
				eachPix[2] = int( (float(eachPix[2])*blueP + float(modif[2])*blue) )
			eachPix = verifIntensity(eachPix)
			
			indexPix = indexPix + 1
		indexRow = indexRow + 1
	if(showImage):
		plt.imshow(tableau)
		plt.show()
	
	return tableau

def TraitementSon(tableau, pathToWave, version, showImage, verbose):
	print('[INFO] Traitement du Son')
	# Ouverture et extraction des donnees
	son = wave.open(pathToWave, 'rb')	# file
	nbCanaux = son.getnchannels()		# int
	poids = son.getsampwidth()			# int
	frameRate = son.getframerate()		# int
	nbFrames = son.getnframes()			# int
	
	# Traitement primaire des donnees
	nbOctetSec = frameRate*poids		# (int) Nombre d'octet par seconde et par cote
	
	
	# Traitement du son
	frames = binascii.hexlify(son.readframes(nbFrames))	# str
	if(verbose):
		print('[INFO] Lenght : ' + str(len(frames)/2/frameRate/nbCanaux/poids) + ' sec |  Poids : ' + str(poids) + ' octets | FrameRate : ' + str(frameRate) + 'Hz')
	
	textHexa = FramesToHexa(frames, poids, verbose)
	textCanaux = SeparationCanaux(textHexa,verbose)
	textMoyenneCanaux = MoySecHex(textCanaux, frameRate, verbose)
	
	
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

def SaveImage(tableau):
	#plt.imshow(tableau)
	#plt.show()
	if(input("Sauver l'image ? yes(1) | no(0) ")):
		newimage = Image.new('RGB', (len(tableau[0]), len(tableau)))
		newimage.putdata([tuple(p) for row in tableau for p in row])
		newimage.save('img/' + raw_input('[INFO] Exportation\nNom de l\'image : ') + '.png')
		print('[INFO] Image Sauvee')
	else:
		print('[INFO] Image Non Sauvee')

def LoadBackImage(absPath):
	print('[INFO] Loading BackImage')
	liste = glob.glob(absPath + "/res/backimage.*")
	for files in liste:
		extension = files.split('backimage.')[1]
		if(extension == 'png'):
			print('[INFO] Extension : png')
		elif(extension == 'jpg'):
			print('[INFO] Extension : jpg\nConversion en png')
			#ConvertJPGToPNG(files)

def MessageFinProgramme():
	soon = []
	soon.append("Traitements de l'image en couleur (et pas noir et blanc)")
	soon.append("Texte en phonetique")
	soon.append("Recherche du texte sur genius.com")
	soon.append("Traitement du son (branch son)")
	#soon.append("")
	
	print("*\n**\n***\n****\n*****")
	print("Fin du programme")
	print("Coming Soon :")
	for module in soon:
		print("\t- " + module)
	print("*****\n****\n***\n**\n*")

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
	
	##### Recherche de l'image et du son a importer
	LoadBackImage(absPath)
	pathToBackImage = absPath + '/res/backimage.png'
	pathToWave = absPath + '/res/son.wav'
	
	##### Mode
	showImage = input("Show Image ? yes(1) | no(0) ")
	verbose = input("Verbose ? yes(1) | no(0) ")
	
	##### Image
	
	# Creation
	tableau = CreerImage(text, 3, showImage, verbose)
	
	# Traitement
	tableau = FocusColors(tableau,  showImage, False)
	tableau = TraitementImage(tableau, pathToBackImage, input("Mode de traitement : "), showImage, verbose)
	tableau = TraitementSon(tableau, pathToWave, 1, showImage, 1)
	
	# Save
	SaveImage(tableau)
	
	#Fin
	MessageFinProgramme()

main()
