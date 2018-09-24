#!/bin/bash

if [ "$1" == "-c" ]; then
	if [ -d ~/GhostColor ]; then
		cd ~/GhostColor
		python /usr/src/TextPaintingProjectConsole.py
	else
		mkdir ~/GhostColor
		cd ~/GhostColor
		python /usr/src/TextPaintingProjectConsole.py
	fi
	
elif [ "$1" == "-g" ]; then
	if [ -d ~/GhostColor ]; then
		cd ~/GhostColor
		python /usr/src/TextPaintingProjectGraphic.py
	else
		mkdir ~/GhostColor
		cd ~/GhostColor
		python /usr/src/TextPaintingProjectGraphic.py
	fi
	
elif [ "$1" == "-h" ]; then
	echo "#######################"
	echo "##### PAGE D'AIDE #####"
	echo "#######################"
	echo "Tapez <ghostcolor -c> pour lancer en mode shell."
	echo "Tapez <ghostcolor -g> pour lancer en mode graphique."
	
else
	echo "Bienvenue à GHOST COLOR"
	echo "Tapez <ghostcolor -h> pour accéder à la page d'aide"
	
fi
