#!/usr/bin/python

# -*- coding: utf-8 -*-

import os
import glob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as smisc
from math import sqrt, pow
import wave
import scipy.io.wavfile as waveF
from numpy.fft import fft
import binascii

#################
##### TOOLS #####
#################

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

################
##### TEXT #####
################

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

def verifIntensity(eachPix):
	for eachColor in eachPix:
		if(eachColor > 255):
			eachColor = 255
		elif(eachColor < 0):
			eachColor = 0
	return eachPix

def TextToVers(text):
	vers = text.split('\n')
	return vers

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

def CreerImage(text, version, showImage, verbose):
	if((version == 1) or (version == 0)):
		print('[INFO] Methode 1 choisie')
		return CreationImage1(text, showImage, verbose)

def CreationImage1(text, showImage, verbose):
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

#################
##### IMAGE #####
#################

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

def TraitementImage(tableau, pathToBackImage, showImage, verbose):
	print('[INFO] Traitement Image')
	version =  input("Mode de traitement : ")
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
		redP = 1.0 - red
		greenP = 1.0 - green
		blueP = 1.0 - blue
	else:
		pourcentageBackImage = input('Pourcentage de BackImage : ')
		red = float(pourcentageBackImage)/100
		green = float(pourcentageBackImage)/100
		blue = float(pourcentageBackImage)/100
		redP = float(100 - pourcentageBackImage)/100
		greenP = float(100 - pourcentageBackImage)/100
		blueP = float(100 - pourcentageBackImage)/100
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

###############
##### SON #####
###############

def LoadWave(absPath):
	print('[INFO] Loading Wave')
	liste = glob.glob(absPath + "/res/son.*")
	for files in liste:
		extension = files.split('son.')[1]
		if(extension == 'wav'):
			print('[INFO] Extension : wav')
		elif(extension == 'mp3'):
			print('[INFO] Extension : mp3\nConversion en wav')
			#ConvertMP3ToWAV(files)

def AnalyseFourier(data,rate,debut,duree):
	start = int(debut*rate)
	stop = int((debut+duree)*rate)
	spectre = np.absolute(fft(data[start:stop]))
	print('[FOURIER] Lenght Spectre : ' + str(len(spectre)) + ' | Max = ' + str(spectre.max()))
	
	return spectre

def MoyFourier1(spectre, index, lenTab, lenSpectre, max):
	sum = 0
	lenFor = lenSpectre/lenTab
	if(lenFor > 0):
		for i in range(lenFor):
			sum = sum + sqrt((pow(spectre[i + (lenFor*index)][0], 2) + pow(spectre[i + (lenFor*index)][1], 2)))
		sum = (sum / lenFor / max) * 255
		
	return sum

def TraitementSon(tableau, pathToWave, showImage, verbose):
	print('[INFO] Traitement du Son')
	version =  input("Mode de traitement : ")
	if(version == 0):
		return tableau
	if(version == 1):
		MethodeSon1(tableau, pathToWave, showImage, verbose)
	
	return tableau

def MethodeSon1(tableau, pathToWave, showImage, verbose):
	# Analyse de Fourier
	print('[INFO] Analyse de Fourier')
	rate, data = waveF.read(pathToWave)
	debut = 0
	duree = data.size/rate
	spectre = AnalyseFourier(data,rate,debut,duree)
	max = spectre.max()
	lenSpectre = len(spectre)
	lenTab = len(tableau)
	pourcentage = float(float(input("Pourcentage d'image d'origine : "))/100)
	for indexLine in range(lenTab):
		valueLine = MoyFourier1(spectre, indexLine, lenTab, lenSpectre, max)
		for i in range(lenTab):
			tableau[i][indexLine][0] = int(tableau[i][indexLine][0]*pourcentage + (1.0-pourcentage)*valueLine)
			tableau[i][indexLine][1] = int(tableau[i][indexLine][1]*pourcentage + (1.0-pourcentage)*valueLine)
			tableau[i][indexLine][2] = int(tableau[i][indexLine][2]*pourcentage + (1.0-pourcentage)*valueLine)
	
	return tableau

###########################
##### CLOSE PROGRAMME #####
###########################

def SaveImage(tableau):
	try:
		plt.imshow(tableau)
		plt.show()
	except:
		print('[ERROR] plt.imshow(); plt.show(); enabled... Please Turn On xming')
	
	if(input("Sauver l'image ? yes(1) | no(0) ")):
		newimage = Image.new('RGB', (len(tableau[0]), len(tableau)))
		newimage.putdata([tuple(p) for row in tableau for p in row])
		newimage.save('img/' + raw_input('[INFO] Exportation\nNom de l\'image : ') + '.png')
		print('[INFO] Image Sauvee')
	else:
		print('[INFO] Image Non Sauvee')

def MessageFinProgramme():
	# Data
	soon = []
	soon.append("Texte en phonetique")
	soon.append("Recherche du texte sur genius.com")
	#soon.append("")
	
	print("*\n**\n***\n****\n*****")
	print("Fin du programme")
	print("Coming Soon :")
	for module in soon:
		print("\t- " + module)
	print("*****\n****\n***\n**\n*")

################
##### MAIN #####
################

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
	LoadWave(absPath)
	pathToWave = absPath + '/res/son.wav'
	
	##### Mode
	showImage = input("Show Image ? yes(1) | no(0) ")
	verbose = input("Verbose ? yes(1) | no(0) ")
	
	##### Image
	
	# Creation
	tableau = CreerImage(text, 1, showImage, verbose)
	
	# Traitement
	tableau = FocusColors(tableau, showImage, False)
	tableau = TraitementImage(tableau, pathToBackImage, showImage, verbose)
	tableau = TraitementSon(tableau, pathToWave, showImage, verbose)
	
	# Save
	SaveImage(tableau)
	
	#Fin
	MessageFinProgramme()

main()
