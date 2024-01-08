# =============== La classe Document ===============
class Document :
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte="", type="") :
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = type

    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\tType: {self.type}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self) :
        return f"{self.titre}, par {self.auteur}"
    
    # Fonction qui renvoie le type du document
    def get_type(self):
        return self.type

# =============== La classe RedditDocument ===============
class RedditDocument(Document) :
	# Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte="", nbr_com=0):
        super().__init__(titre, auteur, date, url, texte, type="Reddit")
        self.nbr_com = nbr_com

    # Fonction qui renvoie le nombre de commentaires du document
    def get_nbr_com(self):
        return self.nbr_com
    
    # Fonction qui permet de définir le nombre de commentaires du document
    def set_nbr_com(self, nbr_com):
        self.nbr_com = nbr_com

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        parent_str = super().__str__()
        return f"{parent_str}, Source: {self.get_type()}\nNombre de commentaires : {self.nbr_com}\n"

# =============== La classe ArxivDocument ===============
class ArxivDocument(Document) :
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        super().__init__(titre, auteur, date, url, texte, type="Arxiv")
        
        # Vérifie si l'auteur est une liste (co-auteurs présents)
        if isinstance(self.auteur, list) :
            # Le premier auteur devient l'auteur principal, les autres sont des co-auteurs
            self.coAuteur = self.auteur[1:]
            self.auteur = self.auteur[0]
        else :
            # Aucun co-auteur s'il n'y a qu'un seul auteur
            self.coAuteur = []

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)        
    def __str__(self):
        return super().__str__() + f" Co-Auteurs : {self.coAuteur}, Source: {self.get_type()}\n"
    
# =============== La classe DocGenerator ===============
class DocGenerator:
    # Méthode statique pour créer des instances de documents en fonction du type
    @staticmethod
    def factory(type, titre):
        if type == "Reddit": return RedditDocument(titre)
        if type == "Arxiv": return ArxivDocument(titre)

        assert 0, "Erreur :" + type