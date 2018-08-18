# TextPaintingProject

Ce programme est destiné à des fins artistiques. Il en est encore au stade de pré-développement et est donc très mal écrit et optimisé.
Le but de cette première version est de voir comment serait le rendu final de l'oeuvre.

-----

## Fonctionnement

* Insérer votre texte brut dans le fichier ./res/textAPeindre.txt
* Renommer l'image en "./res/backimage.png"
* Lancer le script ./TextPaintingProject.py
* Suivre les instruction

---

## Versions de Traitement

1. Intensité moyenne de chaque pixel de l'image (moy) additionnée à l'intensité de la couleur la plus lumineuse de chaque pixel (l'intensité moyenne est divisée par K)
2. Intersité moyenne de chaque pixel de l'image (moy) ajoutée/soustraite à l'image du texte. Les pourcentages sont les pourcentages d'intensité de l'image de fond.

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