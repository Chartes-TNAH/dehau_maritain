# Réseau d'influence Dehau-Maritain


## But de l'application : Le père Pierre-Thomas Dehau o.p. et Jacques Maritain, un réseau d'influence commun à redécouvrir 	

L'application web Réseau d'Influence Dehau-Maritain a pour but de faire redécouvrir le réseau d'influence commun au père Pierre-Thomas Dehau o.p., homme méconnu de son temps, et à Jacques Maritain, philosophe mondialement connu. 
Ce dernier reconnaît devoir beaucoup au père Dehau. Le but est donc de mieux cerner l'un et l'autre par une approche de réseau et de cercles d'appartenance.
Cette application se concentre donc particulièrement sur les personnes fréquentées par un Maritain "première manière", avant son départ aux Etats-Unis, et elle n'est absolument pas exhaustive, les recherches sur le sujet étant encore malheureusement limitées. 

## Description des fonctionnalités de l'application

Cette application permet de :
	- consulter un index des intellectuels, de leurs oeuvres.
	- consulter les notices biobibliographiques des intellectuels
	- faire une recherche rapide
	- faire une recherche à facettes 
	- créer un compte et pouvoir ainsi créer, modifier ou supprimer les publications 
	- télécharger la base de données


## Développement de l'application 

Cette application a été réalisée dans le cadre de l'évaluation du cours Python du Master 2 TNAH à l'Ecole Nationale des Chartes (Paris, Promotion 2020) par Laure Rossignol.
Elle est développée avec le langage Python3 et le framework Flask et s'appuie sur une base de données. Elle utilise également Bootstrap pour la mise en forme graphique.
Ce projet s'appuie largement sur le cours de Monsieur Thibault Clérice, responsable pédagogique du master Technologies Numériques Appliquées à l'Histoire, de l'Ecole Nationale des Chartes, ainsi que des tutoriels de Michel Grinberg.
Il s'inspire également en bonne partie des travaux réalisés par les anciennes promotions ainsi que l'actuelle.

## Installation et premier lancement de l'application (une seule fois)

* Installer Python3
* Cloner ce dépôt Git: `git clone https://github.com/LaureRossignol/dehau_maritain.git`
* Entrer dedans avec la commande `cd dehau_maritain` 
* Installer, configurer et lancer un environnement virtuel avec Python3: `virtualenv -p python3 env` pour l'installation, `source env/bin/activate` pour le lancement
* Taper dans le terminal `pip install flask` pour installer flask dans l'environnement virtuel (à n'exécuter qu'une seule fois)
* Installer les requirements.txt: `pip install -r requirements.txt` 
* Lancer l'application avec la commande `python3 run.py`  

## Lancement de l'application (à chaque fois)
* Entrer dans le dossier avec la commande `cd dehau_maritain` 
* Lancer l'environnemnent virtuel : `source env/bin/activate`
* Lancer l'application avec la commande `python3 run.py`


## Nota 
Les dessins de la page d'accueil ne sont pas libres de droit. Si vous souhaitez les réutiliser, demandez-le à cette adresse : *laurerossignol@yahoo.com* 
