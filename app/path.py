#Obtention du chemin actuel de l'application

import os
#Module nous permettant d'intéragir avec le système sur lequel python est en train de 'tourner'. Ce package permet donc de faire des opérations liées au système

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
#On récupère le nom de dossier du résultat de os.path.abspath(_file_)) qui récupère le chemin absolu dossier du fichier qui comprend ce code
print(chemin_actuel)

templates = os.path.join(chemin_actuel, "dehau_maritain", "templates")
print(templates)