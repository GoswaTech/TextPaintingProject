#!/usr/bin/python

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as smisc
from math import sqrt

def XSize(text):
	ret = (int(sqrt(len(text)/3))+1)
	print('[INFO] X = ' + str(ret))
	return ret

def YSize(text):
	ret = (int(sqrt(len(text)/3))+1)
	print('[INFO] Y = ' + str(ret))
	return ret

def XSize2(text):
	ret = int(len(text)/3)+1
	print('[INFO] X = ' + str(ret))
	return ret

def YSize2(text):
	ret = int(len(text)/3)+1
	print('[INFO] Y = ' + str(ret))
	return ret

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

def CreerImage(imageArray, text, version, showImage, verbose):
	if(version == 1 ):
		print('[INFO] Methode 1 chosie')
		return CreationImage(imageArray, text, showImage, verbose)
	elif(version == 2):
		print('[INFO] Methode 2 choisie')
		return CreationImage2(imageArray, text, showImage, verbose)

def CreationImage(imageArray, text, showImage, verbose):
	print('[INFO] Image en Creation')
	curseur = 0
	newAr = np.array(smisc.imresize(imageArray.copy(), (XSize(text),YSize(text))))
	print('[INFO] Image redimensionne')
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

def CreationImage2(imageArray, text, showImage, verbose):
	print('[INFO] Image2 en Creation')
	curseur = 0
	newAr = np.array(smisc.imresize(imageArray.copy(), (XSize2(text),YSize2(text))))
	print('[INFO] Image redimensionne')
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

def TraitementImage(tableau, pathToBackImage, version, showImage, verbose):
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

def main():
	print('[INFO] Programme Lance')
	text = open('res/textAPeindre.txt').read()
	print('INFO] Text en cache')
	img = Image.open('res/blanc500x500.png')
	print('[INFO] Image Blanche en cache')
	pathToBackImage = 'res/backimage.png'
	print('[INFO] Debut de conversion')
	
	##### Image
	# Nom du Fichier
	nomFichier = raw_input('Nom de l\'image : ')
	
	# Creation
	tableau = CreerImage(img, text, 2, False, False)
	
	# Traitement
	tableau = TraitementImage(tableau, pathToBackImage, input("Mode de traitement : "), True, False)
	
	# Save
	SaveImage('img/' + nomFichier + '.png', tableau)

main()