#Mise en place des classes de la base de données

from .. app import db
#  Importation de la base de données sqlite, stockée dans la variable db

from app.modeles.utilisateurs import User										   
import datetime

# Création du modèle selon celui de la base de données dehau_maritain.sqlite :

# Table d'association nécessaire à la déclaration d'une relation many-to-many entre la table intellectuel et la table organisation dans la db


EtreLieAorganisation = db.Table("etreLieAorganisation",
	db.Column("id", db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True),
	db.Column("org_intel_id", db.Integer, db.ForeignKey("intellectuel.id_intel"), primary_key=True),
	db.Column("org_id", db.Integer, db.ForeignKey("organisation.id_org"), primary_key=True)
	)

class Intellectuel(db.Model):

	__tablename__ = "intellectuel"
	id_intel = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
	prenom = db.Column(db.Text)
	nom = db.Column(db.Text)
	date_naissance = db.Column(db.Text)
	date_mort = db.Column(db.Text)
	profession_biographie = db.Column(db.Text)
	image_lien = db.Column(db.Text)
	biographie = db.Column(db.Text)
	citation_generale = db.Column(db.Text)
	citation_sur_dehau = db.Column(db.Text)
	citation_sur_maritain = db.Column(db.Text)
	# La table d'association (nécessaire pour une relation many-to-many)
	# est indiquée grâce au deuxième argument de 'relationship' : 'secondary = EtreLieAorganisation
	# l'utilisation d'un backref à la place du back_populates permet de directement déclarer au sein de la table organisation l'équivalent de cette relation : (cela "économise" l'écriture d'une relation.
	organisation = db.relationship("Organisation", secondary=EtreLieAorganisation, backref=db.backref("individuals"))
	publications = db.relationship("Publications", back_populates="intellectuel")


	 #Jointures : 
	#Les relations many to one sont identifiées par des clefs étrangères du côté de la relation simple.
	#db.relationship() permet de construire des relations directes entre les objets et de naviguer entre eux. 
	#Cette fonction, contrairement à db.Column(), n'intervient pas sur la structure MySQL mais elle permet simplement de lier les classes.
	oeuvres = db.relationship("Publications", backref="intellectuell", cascade='all, delete, delete-orphan')

	 #Grâce aux suppressions en cascade, lorsqu'un intellectuel est supprimé, les objets qui lui sont enfants/associés le seront également.



#Table décrivant les organisations auxquelles les intellectuels sont rattachés  
class Organisation(db.Model):
	__tablename__ = "organisation"
	id_org = db.Column(db.Integer, unique=True, primary_key=True, nullable=False, autoincrement=True)
	nom_organisation = db.Column(db.Text)
	description_org = db.Column(db.Text)
	intel_id = db.Column(db.Integer, db.ForeignKey('intellectuel.id_intel'))
	intellectuel = db.relationship("Intellectuel", secondary=EtreLieAorganisation, back_populates="organisation")
	

#Table contenant une sélection d'ouvrages écrits par ces intellectuels
class Publications(db.Model):
	__tablename__ = "publications"
	id_publ = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
	titre = db.Column(db.Text)
	date_publ = db.Column(db.Text)
	resume = db.Column(db.Text)
	# publ_intel_id = db.Column(db.Text)
	#Jointure
	#Les relations many to one sont identifiées par des clefs étrangères du côté de la relation simple.
	publications_id_intell = db.Column(db.Integer, db.ForeignKey('intellectuel.id_intel')) #
	intellectuel = db.relationship("Intellectuel", back_populates="publications")

	#db.relationship() permet de construire des relations directes entre les objets et de naviguer entre eux. 
	#Cette fonction, contrairement à db.Column(), n'intervient pas sur la structure MySQL mais elle permet simplement de lier les classes.
	authorships_publications = db.relationship("Authorship_publications", back_populates="publications")

	@staticmethod
	#@staticmethod permet d'intéragir avec une classe pour un objet qui n'existe pas encore.

	def creer_publications(new_titre, new_date_publ, new_resume, id_intel):
		"""
		Fonction qui permet de créer une nouvelle oeuvre et de l'ajouter à la base de données (ajout rendu possible par un utilisateur)
		:param new_titre: titre de l'oeuvre
		:param new_date_publ: date de la publication de l'oeuvre
		:param new_resume : resume de l'oeuvre
		:type param: string
		:returns: tuple (booléen, liste/objet)
		S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
		Sinon, elle renvoie True, suivi de l'objet créé (ici une nouvelle oeuvre).
		"""

		#On crée une liste vide pour les erreurs
		erreurs = []

		#On vérifie que l'utilisateur complète au moins deux champs de données considérés comme essentiels
		if not new_titre:
			erreurs.append("le champ 'titre' est obligatoire")
		if not new_date_publ:
			erreurs.append("le champ 'date de publication' est obligatoire")
		
		#Si on a au moins une erreur, retourner un message d'erreur
		if len(erreurs) > 0:
			return False, erreurs

		#On vérifie que la longueur des caractères de la date ne dépasse pas la limite de 4 (AAAA)
		if new_date_publ :
			if not len(new_date_publ) == 4 :
				erreurs.append("Les dates doivent faire 4 caractères. Format AAAA demandé.")
			if len(erreurs) > 0:
				return False, erreurs

		#On vérifie que l'oeuvre que l'utilisateur veut ajouter n'existe pas déjà dans la base.
		new_publications = Publications.query.filter(db.and_(Publications.titre == new_titre, Publications.date_publ == new_date_publ)).count()
		if new_publications > 0:
			erreurs.append("Cette oeuvre existe déjà dans la base de données")


		 # Si on a au moins une erreur, on affiche un message d'erreur
		if len(erreurs) > 0:
			return False, erreurs

		 # Si on n'a pas d'erreurs, on ajoute une nouvelle entrée dans la table publications avec les champs correspondant aux paramètres du modèle.
		created_publications = Publications(
			titre = new_titre,
			date_publ = new_date_publ,
			resume = new_resume,
			publications_id_intell=id_intel)


		#On ouvre un double bloc "try-except" afin de gérer les erreurs
		try:
			 # On ajoute la publication à la base de donnees
			db.session.add(created_publications)
			db.session.commit()

			return True, created_publications
		#Exécution de except uniquement si une erreur apparaît. 
		except Exception as erreur:
			return False, [str(erreur)]

	# @staticmethod permet d'intéragir avec une classe pour un objet qui n'existe pas encore.
	@staticmethod
	def modifier_publications(Id_publ, Titre, Date_publ, Resume):
		"""
		Fonction qui permet de modifier les informations d'une publication dans la base de données (modifications rendues possibles par un utilisateur).
		:param Id_publ: identifiant numérique de l'oeuvre
		:param Titre: titre de l'oeuvre
		:param Date_publ: Date de la publication de l'oeuvre
		:param Resume : résumé de l'oeuvre
		:type Id_publ: integer
		:type Titre, Date_publ: string
		:returns: tuple (booléen, liste/objet)
		 S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
		Sinon, elle renvoie True, suivi de l'objet mis à jour (ici une oeuvre).
		"""
		#On crée une liste vide pour les erreurs
		erreurs=[]

		#On vérifie que l'utilisateur complète au moins deux champs de données considérés comme essentiels
		if not Titre:
			erreurs.append("le champ 'titre' est obligatoire")
		if not Date_publ:
			erreurs.append("le champ 'date de la publication' est obligatoire")

		#Si on a au moins une erreur, retourner un message d'erreur
		if len(erreurs) > 0:
			return False, erreurs

		#On récupère une publication dans la base grâce à son identifiant
		update_publications = Publications.query.get(Id_publ)

		#On vérifie que l'utilisateur modifie au moins un champ

		if update_publications.titre == Titre \
				and update_publications.date_publ == Date_publ\
				and update_publications.resume == Resume:
			erreurs.append("Aucune modification n'a été réalisée")

		if len(erreurs) > 0:
			return False, erreurs

		#On vérifie que la longueur des caractères de la date ne dépasse pas la limite de 4 (format AAAA)
		if Date_publ :
			if not len(Date_publ) == 4 :
				erreurs.append("Les dates doivent faire 4 caractères. Format AAAA demandé.")
			if len(erreurs) > 0:
				return False, erreurs

		# Si on a au moins une erreur, on affiche un message d'erreur
		if len(erreurs) > 0:
			return False, erreurs

		#S'il n'y a pas d'erreurs, on met à jour les données de la publication :
		else :
			update_publications.titre=Titre
			update_publications.date_publ=Date_publ
			update_publications.resume=Resume

		#On ajoute un bloc "try-except" afin de "gérer" les erreurs
		try:
			# On ajoute la publication à la base de données
			db.session.add(update_publications)
			db.session.commit()

			return True, update_publications

		#Exécution de except uniquement si une erreur apparaît. 
		except Exception as erreur:
			return False, [str(erreur)]

	@staticmethod
	def supprimer_publications(Id_publ):
		"""
		Fonction qui permet de supprimer la notice d'une publication.
		:param Id_publ: identifiant numérique de l'oeuvre
		:type Id_publ: integer
		:returns: booleens
		"""

		#On récupère une publication dans la base grâce à son identifiant
		delete_publications = Publications.query.get(Id_publ)
	
		#On ajoute un bloc "try-except" afin de "gérer" les erreurs
		try:
			#On supprime la publication de la base de données
			db.session.delete(delete_publications)
			db.session.commit()
			return True

		except Exception as erreur:
			return False, [str(erreur)]

#Il faut établir des relations many-to-many entre la table User et les  tables Intellectuel, Publications et Organisation (tables sur lesquelles les utilisateurs peuvent apporter des modifications).
#Pour cela, on crée des tables Authorship.


class Authorship_publications(db.Model):
#On crée notre modèle Authorship pour la table Publications.
	__tablename__="authorship_publications"
	authorship_publications_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
	authorship_publications_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	authorship_publications_id_publ = db.Column(db.Integer, db.ForeignKey('publications.id_publ'))
	authorship_publications_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	#Jointures
	#db.relationship() permet de construire des relations directes entre les objets et de naviguer entre eux. 
	#Cette fonction, contrairement à db.Column(), n'intervient pas sur la structure MySQL mais elle permet simplement de lier les classes.
	user_publications = db.relationship("User", back_populates="author_publications")
	publications = db.relationship("Publications", back_populates="authorships_publications")
