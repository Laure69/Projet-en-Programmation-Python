from author import *
from document import *
import pickle

# Fonction décoratrice pour créer un singleton
def singleton(cls):
    instance =[None]
    def wrapper(*args,**kwargs):
        nonlocal instance
        if instance[0] is None:
            instance[0] = cls(*args,**kwargs)
        return instance[0]
    return wrapper

# =============== La classe Corpus ===============
#@singleton
class Corpus :
    # Initialisation des variables de la classe
    def __init__(self, nom) :
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
    
    # Ajout d'un document au corpus
    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

    # Affiche les documents triés par date
    def showDate(self, n_docs=-1):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]
        for doc in docs:
            print(f"Date: {doc.date}")

    # Affiche les documents triés par titre
    def showTitre(self, n_docs=-1):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        for doc in docs:
            print(f"Titre: {doc.titre}")

    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))
        return "\n".join(list(map(str, docs))) 
    
    # Sauvegarde le corpus dans un fichier binaire
    def save(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)

    # Charge le corpus à partir d'un fichier binaire
    @classmethod
    def load(cls, file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f) 