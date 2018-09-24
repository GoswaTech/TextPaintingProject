# TextPaintingProject

Ce programme est destiné à des fins artistiques. Il en est encore au stade de pré-développement et est donc très mal écrit et optimisé.
Le but de cette première version est de voir comment serait le rendu final de l'oeuvre.

-----

## Dépendances

Ce logiciel a besoin de ces dépendances pour fonctionner :
* python-imaging
* python-numpy
* python-matplotlib
* python-scipy
* python-tk

-----

## Installation

### Avec git clone

```
git clone https://github.com/GoswaTech/TextPaintingProject.git
cd TextPaintingProject
sudo ./setup.sh
```

### Avec la release

```
#Extraire l'archive
cd TextPaintingProject-*.*
sudo ./setup.sh
```
Tout est prêt !

-----

## Fonctionnement

# En Mode Console
`ghostcolor -c`

* Renommer le texte brut en "textAPeindre" dans le dossier "~/GhostColor/res" (le texte doit être un txt)
* Renommer l'image en "backimage" dans le dossier "~/GhostColor/res" (l'image doit être un png)
* Renommer le son en "son" dans le dossier "~GhostColor/res" (le son doit être un wav)
* Suivre les instruction

# En Mode Graphique
`ghostcolor -g`

* Renommer le texte brut en "textAPeindre" dans le dossier "~/GhostColor/res" (le texte doit être un txt)
* Renommer l'image en "backimage" dans le dossier "~/GhostColor/res" (l'image doit être un png)
* Renommer le son en "son" dans le dossier "~GhostColor/res" (le son doit être un wav)
* Suivre les instruction

---

## Versions de Traitement d'Image

1. Intensité moyenne de chaque pixel de l'image (moy) additionnée à l'intensité de la couleur la plus lumineuse de chaque pixel (l'intensité moyenne est divisée par K)
2. Intensité moyenne de chaque pixel de l'image (moy) ajoutée/soustraite à l'image du texte. Les pourcentages sont les pourcentages d'intensité de l'image de fond.
3. Combine chaque couleur de chaque pixel de l'image avec l'image du texte. Possibilité de choisir le pourcentage de red/green/blue ou le pourcentage de la couleur du pixel.

---

## Versions de Traitement du Son

1. Echelle linéaire, valeur absolue du transformé de Fourier en nuances de gris en colonnes sur l'image. Choisir le pourcentage de l'image de base.

---

## Formules utilisées

* Pour le traitement 1
`* moy = (pixRed + pixGreen + pixBlue) / 3`
`* modif = moy / K`
`* colorPixDominant = colorPixDominant + modif`
* Pour le traitement 2
`* moy = (pixRed + pixGreen + pixBlue) / 3`
`* red = red +- moy*pourcentage`
`* green = green +- moy*pourcentage`
`* blue = blue +- moy*pourcentage`