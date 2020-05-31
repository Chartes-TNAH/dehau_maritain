from flask import render_template, url_for
# L'import de render_template permet de relier les templates aux urls - routes
# L'import de url_for permet de construire des URL vers les fonctions et les pages html

from app.app import app 
# Cette commande permet d'importer, depuis le package app, la variable app qui instancie l'application.

# Gestion des erreurs les plus courantes :

@app.errorhandler(404)
def page_introuvable(erreur):
	"""Route qui permet, en cas d'erreur 404 (page introuvable, car mauvaise URL), de renvoyer vers la page 404.html"""
	return render_template("pages/erreurs/404.html"), 404

@app.errorhandler(410)
def page_supprimee(erreur):
	"""Route qui permet, en cas d'erreur 410 (élément supprimé), de renvoyer vers la page 410.html"""
	return render_template("pages/erreurs/410.html")

@app.errorhandler(500)
def probleme_serveur(erreur):
	"""Route qui permet, en cas d'erreur 500 (erreur de serveur interne), de renvoyer vers la page 500.html"""
	return render_template("pages/erreurs/500.html")
