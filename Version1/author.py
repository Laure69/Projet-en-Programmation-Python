# =============== La classe Author ===============
class Author :
    # Initialisation des variables de la classe 
    def __init__(self, name="") :
        self.name = name
        self.ndoc = 0
        self.production = []

    # Fonction pour ajouter une production à l'auteur
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self) :
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"