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

def saveImage(nomImage, tableau):
	newimage = Image.new('RGB', (len(tableau[0]), len(tableau)))
	newimage.putdata([tuple(p) for row in tableau for p in row])
	newimage.save(nomImage)
	print('[INFO] Image Sauvee')

def main():
	print('[INFO] Programme Lance')
	text = open('res/textAPeindre.txt').read()
	print('INFO] Text en cache')
	pathToFile = 'res/blanc500x500.png'
	img = Image.open(pathToFile)
	print('[INFO] Image Blanche en cache')
	print('[INFO] Debut de conversion')
	
	##### Image
	# Nom du Fichier
	nomFichier = raw_input('Nom de l\'image : ')
	
	# Creation
	tableau = CreerImage(img, text, 2, False, False)
	
	# Save
	saveImage('img/' + nomFichier + '.png', tableau)

main()