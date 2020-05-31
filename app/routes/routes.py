#Définition des url et des fonctions définissant le contenu des pages associées

from flask import render_template, url_for, request, send_file, flash, redirect
# L'import de render_template permet de relier les templates aux urls - routes
# L'import de url_for permet de construire des URL vers les fonctions et les pages html
# L'import de la commande request permet d'importer les noms de types d'objets moins courant que int ou str, et de pouvoir ainsi les utiliser
# dans des fonctions tels que isinstance.()
# L'import de send_file permet d'envoyer des fichiers au client
# L'import de flash permet de produire des messages d'alertes
# L'import de redirect permet de créer des fonctions qui retournent une redirection vers l'url d'une autre route

from sqlalchemy import and_, or_
# Cette commande permet d'utiliser les opérateurs 'and' et 'or' dans les fonctions de requêtage de notre la de données

from flask_login import login_user, current_user, logout_user, login_required
#login_user : valide l'authenfication
#current_user : permet d'obtenir l'utilisateur courant
#logout_user : permet la déconnexion
#login_required : limite la capacité d'accès à une page

from app.app import app, login
#A partir du fichier app.py, contenu dans le dossier app, on importe la variable app, correspondant à l'application.
#On importe également login, destiné à la gestion des utilisateurs

#On importe les classes, disponibles dans donnees.py et utilisateurs.py, de notre modèle de données. Cela permettra ensuite de les requêter :
from app.modeles.donnees import Intellectuel, Publications, Organisation, EtreLieAorganisation
from app.modeles.utilisateurs import User

from app.constantes import resultats_par_page
#A partir du fichier constantes.ipy, contenu dans le dossier app, on importe la variable resultats_par_page

#Les commandes suivantes permettent de créer différentes routes, qui correspondent à l'URL des différents pages de l'application

###PAGE D'ACCUEIL, DE NOTICE, INDEX###

@app.route('/')
def accueil ():
	"""
	Route permettant l'affichage d'une page d'accueil
	:return : affichage du template accueil.html
	"""
	return render_template("pages/accueil.html", nom="dehau_maritain")
	# La fonction render_template prend comme premier argument le chemin du template et en deuxième des arguments nommés, qui
	# peuvent ensuite être réutilisés en tant que variables dans les templates.

@app.route("/index_intellectuels")
def index_intellectuels() :
	"""
	Route permettant l'affichage de l'index des intellectuels enregistrés
	:return : affichage du template index_intellectuels.html
	"""
	titre="index_intellectuels"

	#On vérifie que la base de données n'est pas vide
	intellectuells = Intellectuel.query.all()
	

	if len(intellectuells) == 0:
		intellectuells = ''
		return render_template("pages/index_intellectuels.html", intellectuells=intellectuells, titre=titre)
	else : 
		page = request.args.get("page", 1)

		if isinstance(page, str) and page.isdigit():
			page = int(page)
		else:
			page = 1

	intellectuells = Intellectuel.query.order_by(Intellectuel.nom
			).paginate(page=page, per_page=resultats_par_page)
	return render_template("pages/index_intellectuels.html", nom="dehau_maritain", intellectuells=intellectuells, titre=titre)


@app.route('/intellectuell/<int:id_intel>')
def intellectuell(id_intel):
	"""Route permettant l'affichage des données concernant un intellectuel
	:param id_intel : identifiant numérique de l'intellectuel
	:return : affichage du template intellectuell.html
	"""
	unique_intell = Intellectuel.query.get(id_intel)
	#On fait des jointures pour pouvoir afficher sur la page des intellectuels des données provenant des Publications
	oeuvres = unique_intell.oeuvres
	return render_template("pages/intellectuell.html", nom="dehau_maritain", intellectuell=unique_intell, oeuvres=oeuvres)

@app.route("/index_publication")
def index_publication() :
	"""
	Route permettant l'affichage de l'index des publications enregistrées
	:return : affichage du template index_publication.html
	"""
	titre="index_publication"

	#On vérifie que la base de données n'est pas vide
	oeuvres = Publications.query.all()

	if len(oeuvres) == 0:
		return render_template("pages/index_publication.html", oeuvres=oeuvres, titre=titre)
	else : 
		page = request.args.get("page", 1)

		if isinstance(page, str) and page.isdigit():
			page = int(page)
		else:
			page = 1

	oeuvres = Publications.query.order_by(Publications.titre
			).paginate(page=page, per_page=resultats_par_page)
	return render_template("pages/index_publication.html", nom="dehau_maritain", oeuvres=oeuvres, titre=titre)

@app.route("/intellectuell/oeuvre/<int:id_publ>")
def oeuvre(id_publ):
	"""
	Route permettant d'afficher les données d'une oeuvre
	:param id_publ : idenfiant numérique de l'oeuvre de l'intellectuel'
	:return : affichage du template oeuvre.html
	"""
	unique_oeuvre = Publications.query.get(id_publ)
	#On crée une jointure pour pouvoir afficher sur les pages concernant des oeuvres le nom des intellectuels.
	intellectuell = unique_oeuvre.intellectuell
	return render_template("pages/oeuvre.html", nom="dehau_maritain", oeuvre=unique_oeuvre, intellectuell=intellectuell)
	

###AJOUT, SUPPRESSION, MODIFICATION###

@app.route("/intellectuell/<int:id_intel>/creer_oeuvre", methods=["GET", "POST"])
@login_required
def creation_oeuvre(id_intel):
	""" 
	Route permettant à l'utilisateur de créer une notice d'oeuvre 
	:param id_intel : identifiant de l'intellectuel
	:return : affichage du template creer_oeuvre.html ou redirection
	"""
	
	intellectuel = Intellectuel.query.get(id_intel)

	if request.method == "POST":
		statut, donnees = Publications.creer_oeuvres(
		new_titre = request.form.get("new_titre", None),
		new_date_publ = request.form.get("new_date_premiere_pub", None),
		new_resume = request.form.get("resume", None), 
		id_intel = id_intel
		)

		if statut is True:
			flash("Ajout d'une nouvelle oeuvre", "success")
			return redirect("/index_intellectuels")
		else:
			flash("L'ajout d'une nouvelle oeuvre a échoué pour les raisons suivantes : " + ", ".join(donnees), "danger")
			return render_template("pages/creer_oeuvre.html", intellectuell=intellectuel)
	else:
		return render_template("pages/creer_oeuvre.html", nom="dehau_maritain", intellectuell=intellectuel)

@app.route("/modifier_oeuvre/<int:identifier>", methods=["POST", "GET"])
@login_required
def modification_oeuvre(identifier):
	"""
	Route gérant la modification d'une oeuvre
	:param id_publ: identifiant de l'oeuvre
	:return : affichage du template modifier_oeuvre.html ou redirection
	"""
	# On renvoie sur la page html les éléments de l'objet oeuvre correspondant à l'identifiant de la route
	if request.method == "GET":
		oeuvre_a_modifier = Publications.query.get(identifier)
		return render_template("pages/modifier_oeuvre.html", oeuvre=oeuvre_a_modifier)

	# on récupère les données du formulaire modifié
	else:
		statut, donnees= Publications.modifier_publications(
			Id_publ=identifier,
			Titre=request.form.get("Titre", None),
			Date_publ=request.form.get("Date_publ", None),
			Resume = request.form.get("Resume", None), 
		)

		if statut is True:
			flash("Modification réussie !")
			return redirect ("/index_oeuvres")
		else:
			flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees))
			oeuvre_a_modifier = Publications.query.get(identifier)
			return render_template("pages/modifier_oeuvre.html", nom="dehau_maritain", oeuvre=oeuvre_a_modifier)

@app.route("/supprimer_oeuvre/<int:identifier>", methods=["POST", "GET"])
@login_required
def suppression_oeuvre(identifier):
	""" 
	Route pour supprimer une oeuvre dans la base
	:param identifier : identifiant de l'oeuvre'
	:return : affichage du template supprimer_oeuvre.html ou redirection
	"""
	oeuvre_a_supprimer = Publications.query.get(identifier)

	if request.method == "POST":
		statut = Publications.supprimer_oeuvres(
			Id_publ=identifier
		)

		if statut is True:
			flash("Suppression réussie !")
			return redirect("/index_oeuvres")
		else:
			flash("Echec de la suppression...")
			return redirect("/index_oeuvres")
	else:
		return render_template("pages/supprimer_oeuvre.html", nom="dehau_maritain", oeuvre=oeuvre_a_supprimer)


###GESTION DES UTILISATEURS###

@app.route("/register", methods=["GET", "POST"])
def inscription():
	"""
	Route gérant les inscriptions
	:return : affichage du template inscription.html ou redirection
	"""
	# Si on est en POST, cela veut dire que le formulaire a été envoyé
	if request.method == "POST":
		statut, donnees = User.creer(
			login=request.form.get("login", None),
			email=request.form.get("email", None),
			nom=request.form.get("nom", None),
			motdepasse=request.form.get("motdepasse", None)
		)
		if statut is True:
			flash("Enregistrement effectué. Identifiez-vous maintenant")
			return redirect("/")
		else:
			flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees))
			return render_template("pages/inscription.html", nom="dehau_maritain")
	else:
		return render_template("pages/inscription.html", nom="dehau_maritain")

@app.route("/connexion", methods=["POST", "GET"])
def connexion():
	"""
	Route gérant les connexions
	:return : affichage du template connexion.html ou redirection
	"""
	if current_user.is_authenticated is True:
		flash("Vous êtes déjà connecté")
		return redirect("/")

	# Si on est en POST, cela veut dire que le formulaire a été envoyé
	if request.method == "POST":
		utilisateur = User.identification(
			login=request.form.get("login", None),
			motdepasse=request.form.get("motdepasse", None)
		)
		if utilisateur:
			flash("Connexion effectuée")
			login_user(utilisateur)
			return redirect("/")
		else:
			flash("Les identifiants n'ont pas été reconnus")

	return render_template("pages/connexion.html", nom="dehau_maritain")
login.login_view = 'connexion'

@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
	"""
	Route gérant les déconnexions
	:return : redirection vers la page d'accueil
	"""
	if current_user.is_authenticated is True:
		logout_user()
	flash("Vous êtes déconnecté")
	return redirect("/")


###RECHERCHES, RESULTATS, TELECHARGEMENTS###


#Recherche
@app.route("/recherche")
def recherche():
	"""
	Route permettant d'effectuer de la recherche plein-texte
	:return : affichage du template recherche.html
	"""
	motclef = request.args.get("keyword", None)
	page = request.args.get("page", 1)
	
	if isinstance(page, str) and page.isdigit():
		page = int(page)
	else :
		page = 1

	# On crée une liste vide de résultat (qui restera vide par defaut si on n'a pas de mot clef)
	resultats = []

	titre = "Recherche"
	if motclef:
	#Si on un mot-clef, on requête la table intellectuel de notre base de données pour vérifier s'il y a des correspondances entre le mot entré par l'utilisateur-rice et les données de notre table
		resultats = Intellectuel.query.filter(
			or_(
				Intellectuel.nom.like("%{}%".format(motclef)),
				Intellectuel.prenom.like("%{}%".format(motclef)),
				Intellectuel.date_naissance.like("%{}%".format(motclef)),
				Intellectuel.date_mort.like("%{}%".format(motclef)),
				Intellectuel.profession_biographie.like("%{}%".format(motclef)),
				Intellectuel.image_lien.like("%{}%".format(motclef)),
				Intellectuel.biographie.like("%{}%".format(motclef)),
				Intellectuel.citation_generale.like("%{}%".format(motclef)),
				Intellectuel.citation_sur_dehau.like("%{}%".format(motclef)),
				Intellectuel.citation_sur_maritain.like("%{}%".format(motclef)),
				)
		).order_by(Intellectuel.nom.asc()).paginate(page=page, per_page=resultats_par_page)
		titre = "Résultat pour la recherche '" + motclef + "'"
	return render_template("pages/recherche.html", resultats=resultats, titre=titre, keyword=motclef)


#Téléchargement
@app.route('/telechargement')
def telechargement():
	"""Route permettant d'afficher la page telechargement.html"""
	return render_template("pages/telechargement.html")

@app.route('/download')
def download():
	"""Route permettant à l'utilisateur de télécharger le fichier prosopochartes.sqlite (base de données sur laquelle se base l'application)"""
	f = '../dehau_maritain.sqlite'
	return send_file(f, attachment_filename='dehau_maritain.sqlite', as_attachment=True)


