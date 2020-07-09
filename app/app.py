#Initialisation et configuration

from flask import Flask
# Import de Flask depuis la librairie flask

from flask_sqlalchemy import SQLAlchemy
# Import de SQLAlchemy, qui permet de lier la base de données à l'application, et de la requêter

from flask_login import LoginManager
#On installe flask_login, qui permet de gérer les utilisateurs

import os
# Le module os de python permet d'interagir avec le système sur lequel python est en train de "tourner".

# from .constantes import SECRET_KEY
#On importe depuis le fichier constantes.py le SECRET_KEY


chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")
# Ces trois "commandes sont liées au module os : 
# on indique à quel endroit est la page de base du site et, depuis cette dernière,
# comment accéder aux différents fichiers stockés en local (déclarer où se trouve le dossier templates sera
# notamment très utile pour permettre d'afficher les images par la suite).

app = Flask(
	__name__,  
	template_folder=templates, 
	static_folder=statics)

# Instanciation de l'application : on lui ajoute deux arguments qui permettent de faire le lien
# vers les dossiers déclarés via les commandes os.
# Selon le manuel de Grinberg, _name_ est une variable Python prédéfinie qui prend le nom du module dans lequel elle est
# utilisée.
# app est ici une variable définie comme appartenant à la classe Flask, à ne pas confondre avec le package app (initialisé
# avec le fichier __init__.py.) et qui contient l'application.


app.config['SECRET_KEY'] = '5F3EAXjUf?%,)h#R92y9aq5'
# Le secret key est un paramètre utilisé pour les sessions ou tout ce qui impliquerait des éléments de sécurité avancée 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../doc/dehau_maritain.sqlite'
# Lien avec la base de données sqlite

app.config['SQLALCHEMY_ECHO'] = True
# Cette commande permet d'afficher dans le terminal le détail des requêtes effectuées par sqlalchemy.

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Instanciation du mode debug, cette fonction est liée au fichier .flaskenv

#app.config['DEBUG'] = True #mise en commentaire pour test.

db = SQLAlchemy(app)
# Intégration de l'extension SQLAlchemy à l'application Flask ; la base de données est stockée dans la variable db

login = LoginManager(app)
# On met en place la gestion d'utilisateurs

from .routes import routes, errorhandler
# Cette commande permet de relier les routes - urls à l'application. Elle se situe en dernier car routes a besoin de
# la variable app pour fonctionner. Ceci permet d'éviter des erreurs de code.
# Sur le même modèle, on relie également les fonctions qui gèrent les erreurs à l'application.

