#!/bin/bash

if [ "$1" == "-c" ]; then
	if [ -d ~/GhostColor ]; then
		cd ~/GhostColor
		python /usr/src/GhostColor/TextPaintingProjectConsole.py
	else
		mkdir ~/GhostColor
		mkdir ~/GhostColor/res
		echo "Ecrire le texte ici..." > ~/GhostColor/res/textAPeindre.txt
		cd ~/GhostColor
		python /usr/src/GhostColor/TextPaintingProjectConsole.py
	fi
	
elif [ "$1" == "-g" ]; then
	if [ -d ~/GhostColor ]; then
		cd ~/GhostColor
		python /usr/src/GhostColor/TextPaintingProjectGraphic.py
	else
		mkdir ~/GhostColor
		mkdir ~/GhostColor/res
		echo "Ecrire le texte ici..." > ~/GhostColor/res/textAPeindre.txt
		cd ~/GhostColor
		python /usr/src/GhostColor/TextPaintingProjectGraphic.py
	fi
	
elif [ "$1" == "-h" ]; then
	echo "#######################"
	echo "##### PAGE D'AIDE #####"
	echo "#######################"
	echo "Tapez <ghostcolor -c> pour lancer en mode shell."
	echo "Tapez <ghostcolor -g> pour lancer en mode graphique."
	echo "Tapez <sudo ghostcolor --uninstall> pour désinstaller GhostColor."
	
elif [ "$1" == "--uninstall" ]; then
	echo "Suppression de /usr/src/GhostColor"
	rm -r /usr/src/GhostColor
	echo "Suppression de /usr/bin/ghostcolor"
	rm /usr/bin/ghostcolor
	echo "Désintallation terminée, il ne vous reste plus que le dossier ~/GhostColor"
	
else
	echo "Bienvenue à GHOST COLOR"
	echo "Tapez <ghostcolor -h> pour accéder à la page d'aide"
	
fi
