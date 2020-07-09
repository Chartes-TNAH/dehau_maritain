#Fichier qui permet d'utiliser ce qui est dans l'application.

from app.app import app 
#A partir du fichier app.py, contenu dans le dossier app, on importe la variable app, correspondant à l'application.
from app.app import db


# db.create_all()


if __name__ == "__main__":
	#On vérifie que le ficher est celui couramment exécuté
	app.run(debug=True)
# On lance un serveur de test via app.run()

