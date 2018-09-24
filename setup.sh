#!/bin/bash
if [ "$1" == "--dep" ]; then
	### Installation des dépendances
	echo "Mise a jour des dépôts..."
	apt-get update
	echo "Installation des dépendances"
	apt-get install python-imaging python-numpy python-matplotlib python-scipy python-tk
fi

# Installation du code	
echo "Installation des sources dans /usr/src/GhostColor"
cp -R src/ /usr/src/GhostColor

echo "Installation de la commande dans /usr/bin/GhostColor"
cp GhostColor.sh /usr/bin/ghostcolor
chmod 755 /usr/bin/ghostcolor

# Installation des dossiers exports
echo "Installation des dossiers ~/GhostColor"
mkdir ~/GhostColor
mkdir ~/GhostColor/res

# Installation Terminée
echo "Installation réussie"
echo "Vous pouvez supprimer le dossier, tout a été copié dans les dossiers /usr/bin/ et /usr/src/"
echo "Lancez la commande <ghostcolor -h> pour accéder au manuel"