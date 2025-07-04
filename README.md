# Nom final de la formation

Ce dossier Repository est lié au cours `Nom final de la formation`. Le cours entier est disponible sur [LinkedIn Learning][lil-course-url].

![Nom final de la formation][lil-thumbnail-url] 

Ce cours est intégré à GitHub Codespaces, un environnement de développement instantané « dans le nuage » qui offre toutes les fonctionnalités de votre IDE préféré sans nécessiter de configuration sur une machine locale. Avec Codespaces, vous pouvez vous exercer à partir de n'importe quelle machine, à tout moment, tout en utilisant un outil que vous êtes susceptible de rencontrer sur votre lieu de travail. Consultez la vidéo "Utiliser Codespaces sur GitHub" pour savoir comment démarrer.    

DESCRIPTION DE LA FORMATION

## Instructions

Ce dossier Repository a des branches pour chacune des vidéos du cours. Vous pouvez utiliser le menu des Branches sur GitHub afin d’accéder aux passages qui vous intéressent. Vous pouvez également rajouter `/tree/BRANCH_NAME` à l’URL afin d’accéder à la branche qui vous intéresse. 

## Branches

Les branches sont structurées de manière à correspondre aux vidéos du cours. La convention de nommage est : `CHAPITRE#_VIDEO#`. Par exemple, la branche nommée`02_03` correspond au second chapitre, et à la troisième vidéo de ce chapitre. Certaines branches ont un état de départ et de fin.  
La branche `02_03_d` correspond au code du début de la vidéo.  
La branche `02_03_f` correspond au code à la fin de la vidéo.  
La branche master correspond au code à la fin de la formation. 

Lors d'un changement de branche après avoir modifier un fichier, vous pourriez rencontrer le message d'erreur suivant :
When switching from one exercise files branch to the next after making changes to the files, you may get a message like this:

    error: Your local changes to the following files would be overwritten by checkout:        [files]
    Please commit your changes or stash them before you switch branches.
    Aborting

Afin de résoudre ce problème :
	
    Ajouter les changements au git en utilisant la commande suivante : git add .
	Faire un commit en utilisant la commande suivante : git commit -m "some message"

## Installation

1. Pour utiliser ces fichiers d’exercice, vous avez besoin de : 
   - Une version de Python récente
   - Un IDE Python (VSCode, PyCharm, etc.)
2. Clonez ce dossier Repository sur votre machine locale (Mac), CMD (Windows), ou sur un outil GUI tel que SourceTree. 
3. Activez l'environnement virtuel python
4. Installez les dépendances avec la commande `pip install -r requirements.txt`
5. Migrez les bases de données avec la commande `python manage.py migrate`


### Formateur

**Sylvain Labasse** 

 Retrouvez mes autres formations sur [LinkedIn Learning][lil-URL-trainer].

[0]: # (Replace these placeholder URLs with actual course URLs)
[lil-course-url]: https://www.linkedin.com
[lil-thumbnail-url]: https://media.licdn.com/dms/image/v2/D4E0DAQG0eDHsyOSqTA/learning-public-crop_675_1200/B4EZVdqqdwHUAY-/0/1741033220778?e=2147483647&v=beta&t=FxUDo6FA8W8CiFROwqfZKL_mzQhYx9loYLfjN-LNjgA
[lil-URL-trainer]: https://www.linkedin.com/learning/instructors/sylvain-labasse

[1]: # (End of FR-Instruction ###############################################################################################)
