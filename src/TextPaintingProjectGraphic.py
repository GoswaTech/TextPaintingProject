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
import Tkinter
import ttk
from tkMessageBox import *

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
			#ConvertJPGTkinter.TOPNG(files)

def TraitementImage(tableau, pathToBackImage, showImage, verbose):
	print('[INFO] Traitement Image')
	version =  versionImage.get()
	if(version == 0):
		return tableau
	if(version == 1):
		Methode1(tableau, pathToBackImage, showImage, verbose)
	
	return tableau

def Methode1(tableau, pathToBackImage, showImage, verbose):
	print('[INFO] Methode 3')
	img = Image.open(pathToBackImage)
	imgAr = np.array(smisc.imresize(img.copy(), (len(tableau[0]),len(tableau))))
	print('[INFO] BackImage en cache et redimonsionne')
	
	pourcentageBackImage = float(valueScaleImage.get())
	print('[INFO] Pourcentage de BackImage : ' + str(valueScaleImage.get()) + '%')
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
	version =  versionSon.get()
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
	pourcentage = float(float(valueScaleSon.get())/100)
	print('[INFO] Pourcentage Image Origine : ' + str(valueScaleSon.get()) + '%')
	for indexLine in range(lenTab):
		valueLine = MoyFourier1(spectre, indexLine, lenTab, lenSpectre, max)
		for i in range(lenTab):
			tableau[i][indexLine][0] = int(tableau[i][indexLine][0]*pourcentage + (1.0-pourcentage)*valueLine)
			tableau[i][indexLine][1] = int(tableau[i][indexLine][1]*pourcentage + (1.0-pourcentage)*valueLine)
			tableau[i][indexLine][2] = int(tableau[i][indexLine][2]*pourcentage + (1.0-pourcentage)*valueLine)
	
	return tableau

#####################
##### GRAPHIQUE #####
#####################

def ButtonSave():
	global tableauFinal
	
	#Save
	SaveImage(tableauFinal)
	
	#Fin
	MessageFinProgramme()
	
	##### Destruction des pack
	entrySave.pack_forget()
	boutonSave.pack_forget()
	boutonSkip.pack_forget()
	
	ParametresScreen()

def ButtonSkip():
	#Fin
	MessageFinProgramme()
	
	##### Destruction des pack
	entrySave.pack_forget()
	boutonSave.pack_forget()
	boutonSkip.pack_forget()
	
	ParametresScreen()

def Conversion():
	##### Destruction des pack
	fenetreParametresText.pack_forget()
	fenetreParametresImage.pack_forget()
	fenetreParametresSon.pack_forget()
	boutonConversion.pack_forget()
	
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
	#showImage = input("Show Image ? yes(1) | no(0) ")
	showImage = False
	#verbose = input("Verbose ? yes(1) | no(0) ")
	verbose = False
	
	##### Traitement
	
	# TEXT
	progressBarText.pack(side=Tkinter.TOP)
	progressBarText.start()
	tableau = CreerImage(text, versionText.get(), showImage, verbose)
	tableau = FocusColors(tableau, showImage, False)
	progressBarText.pack_forget()
	
	# IMAGE
	progressBarImage.pack(side=Tkinter.TOP)
	progressBarImage.start()
	tableau = TraitementImage(tableau, pathToBackImage, showImage, verbose)
	progressBarImage.pack_forget()
	
	# SON
	progressBarSon.pack(side=Tkinter.TOP)
	progressBarSon.start()
	tableau = TraitementSon(tableau, pathToWave, showImage, verbose)
	progressBarSon.pack_forget()
	
	global tableauFinal
	tableauFinal = tableau
	
	##### Construction des pack
	SaveScreen()

def SaveScreen():
	# - - - -#
	# DROITE #
	#- - - - #
	
	#| SAVE
	entrySave.pack()
	boutonSave.pack()
	boutonSkip.pack()

def ParametresScreen():
	# - - - -#
	# GAUCHE #
	#- - - - #
	
	fenetreGauche.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=0)
	
	#| TEXT
	fenetreText.pack(side=Tkinter.TOP, fill=Tkinter.X, expand=0)
	
	#-| FichierText
	fenetreFichierText.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=0)
	labelText.pack(fill=Tkinter.X, expand=0)
	
	#-| ParametresText
	fenetreParametresText.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=0)
	boutonVersionText1.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=0)
	
	
	#| IMAGE
	fenetreImage.pack(side=Tkinter.TOP, fill=Tkinter.X, expand=0)
	
	#-| FichierImage
	fenetreFichierImage.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=0)
	labelImage.pack(fill=Tkinter.X, expand=0)
	
	#-| ParametresImage
	fenetreParametresImage.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=0)
	boutonVersionImage0.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=0)
	boutonVersionImage1.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=0)
	scaleImage.pack(side=Tkinter.LEFT)
	
	
	#| SON
	fenetreSon.pack(side=Tkinter.TOP, fill=Tkinter.X, expand=0)
	
	#-| FichierSon
	fenetreFichierSon.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=0)
	labelSon.pack(fill=Tkinter.X, expand=0)

	#-| ParametresSon
	fenetreParametresSon.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=0)
	boutonVersionSon0.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=0)
	boutonVersionSon1.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=0)
	scaleSon.pack(side=Tkinter.LEFT)
	
	
	# - - - -#
	# DROITE #
	#- - - - #
	
	fenetreDroite.pack(side=Tkinter.LEFT)
	
	#| CONVERT
	boutonConversion.pack()
	
	# - - - -#
	# SELECT #
	#- - - - #
	
	boutonVersionText1.select()
	boutonVersionSon1.select()
	boutonVersionImage1.select()

###########################
##### CLOSE PROGRAMME #####
###########################

def SaveImage(tableau):
	if askyesno("Save Image", "Etes-vous sur de vouloir enregistrer l'image ?"):
		newimage = Image.new('RGB', (len(tableau[0]), len(tableau)))
		newimage.putdata([tuple(p) for row in tableau for p in row])
		print('[INFO] Exportation')
		newimage.save('img/' + nameSave.get() + '.png')
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

#-------------------------
# Initialisation de Tkinter
#-------------------------

mainTk = Tkinter.Tk()
mainTk.title("GhostColor")

#-------------------------
# Variables Globales
#-------------------------

global tableauFinal

#-------------------------
# Tkinter
#-------------------------

# - - - -#
# GAUCHE #
#- - - - #

fenetreGauche = Tkinter.Frame(mainTk)

#| TEXT
fenetreText = Tkinter.Frame(fenetreGauche)

#-| FichierText
fenetreFichierText = Tkinter.LabelFrame(fenetreText, text="TEXT")
labelText = Tkinter.Label(fenetreFichierText, text="------------------------------------\ntextAPeindre.txt\n------------------------------------")
progressBarText = ttk.Progressbar(fenetreFichierText, orient="horizontal", length=150, mode="indeterminate")

#-| ParametresText
fenetreParametresText = Tkinter.LabelFrame(fenetreText, text="Parametres TEXT")

#--| RadioButtons
versionText = Tkinter.IntVar()
boutonVersionText1 = Tkinter.Radiobutton(fenetreParametresText, text="V1", variable=versionText, value=1, indicatoron=0)


#| IMAGE
fenetreImage = Tkinter.Frame(fenetreGauche)

#-| FichierImage
fenetreFichierImage = Tkinter.LabelFrame(fenetreImage, text="IMAGE")
labelImage = Tkinter.Label(fenetreFichierImage, text="------------------------------------\nbackimage.png\n------------------------------------")
progressBarImage = ttk.Progressbar(fenetreFichierImage, orient="horizontal", length=150, mode="indeterminate")

#-| ParametresImage
fenetreParametresImage = Tkinter.LabelFrame(fenetreImage, text="Parametres IMAGE")

#--| RadioButtons
versionImage = Tkinter.IntVar()
boutonVersionImage0 = Tkinter.Radiobutton(fenetreParametresImage, text="V0", variable=versionImage, value=0, indicatoron=0)
boutonVersionImage1 = Tkinter.Radiobutton(fenetreParametresImage, text="V1", variable=versionImage, value=1, indicatoron=0)

#--| Scales
valueScaleImage = Tkinter.DoubleVar()
scaleImage = Tkinter.Scale(fenetreParametresImage, orient='horizontal', from_=0, to=100, resolution=0.5, tickinterval=20, length=400, label="BackImage (%)", variable=valueScaleImage)


#| SON
fenetreSon = Tkinter.Frame(fenetreGauche)

#-| FichierSon
fenetreFichierSon = Tkinter.LabelFrame(fenetreSon, text="SON")
labelSon = Tkinter.Label(fenetreFichierSon, text="------------------------------------\nson.wav\n------------------------------------")
progressBarSon = ttk.Progressbar(fenetreFichierSon, orient="horizontal", length=150, mode="indeterminate")

#-| ParametresSon
fenetreParametresSon = Tkinter.LabelFrame(fenetreSon, text="Parametres SON")

#--| RadioButtons
versionSon = Tkinter.IntVar()
boutonVersionSon0 = Tkinter.Radiobutton(fenetreParametresSon, text="V0", variable=versionSon, value=0, indicatoron=0)
boutonVersionSon1 = Tkinter.Radiobutton(fenetreParametresSon, text="V1", variable=versionSon, value=1, indicatoron=0)

#--| Scales
valueScaleSon = Tkinter.DoubleVar()
scaleSon = Tkinter.Scale(fenetreParametresSon, orient='horizontal', from_=0, to=100, resolution=0.5, tickinterval=20, length=400, label="Image d'origine (%)", variable=valueScaleSon)

# - - - -#
# DROITE #
#- - - - #

fenetreDroite = Tkinter.Frame(mainTk)

#| CONVERT
boutonConversion = Tkinter.Button(fenetreDroite, text="C\nO\nN\nV\nE\nR\nT", command=Conversion)

#| SAVE
nameSave = Tkinter.StringVar() 
nameSave.set("nomImage")
entrySave = Tkinter.Entry(fenetreDroite, textvariable=nameSave, width=30)
boutonSave = Tkinter.Button(fenetreDroite, text="Save", command=ButtonSave)
boutonSkip = Tkinter.Button(fenetreDroite, text="Skip", command=ButtonSkip)

#-------------------------
# Mise en Page
#-------------------------

ParametresScreen()

#-------------------------
# Lancement de la Loop
#-------------------------

mainTk.mainloop()