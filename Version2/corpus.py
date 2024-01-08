from author import *
from document import *
import pickle
import re
import pandas as pd

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
        self.texte_intégral = ""
        self.vocabulaire = set()
    
    # Ajout d'un document au corpus
    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
        self.texte_intégral += doc.texte + ""

    # Affiche les documents triés par date
    def showDate(self, n_docs=-1):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]
        for doc in docs:
            print(f"Document: {doc.titre} - Date: {doc.date}")

    # Affiche les documents triés par titre
    def showTitre(self, n_docs=-1):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        for doc in docs:
            print(f"Document: {doc.titre} - Date: {doc.date}")

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
    
    def concatenate(self):
        return " ".join([doc.texte for doc in self.id2doc.values()])

    def search(self, keyword):
        if not self.texte_intégral :
            self.texte_intégral = self.concatenate()
        
        matches = re.finditer(keyword, self.texte_intégral, re.IGNORECASE)
        passages = list(set(match.group() for match in matches))

        return passages
    
    def concorde(self, keyword, context_size=20) :
        if not self.texte_intégral :
            self.texte_intégral = self.concatenate()
        
        pattern = re.compile(f'(.{{0,{context_size}}})({keyword})(.{{0,{context_size}}})', re.IGNORECASE)
        matches = pattern.finditer(self.texte_intégral)

        concordance_data = []

        for match in matches:
            left_context = match.group(1)
            keyword_found = match.group(2)
            right_context = match.group(3)

            concordance_data.append({
                'contexte gauche': left_context,
                'motif trouve': keyword_found,
                'contexte droit': right_context
            })

        concordance_df = pd.DataFrame(concordance_data)
        return concordance_df
        
    def construire_vocabulaire(self):
        if not self.texte_intégral:
            self.texte_intégral = self.concatenate()

        vocabulaire_set = set()

        for doc in self.id2doc.values():
            texte_doc_nettoye = nettoyer_texte(doc.texte)
            # print(texte_doc_nettoye)
            mots = texte_doc_nettoye.split()
            vocabulaire_set.update(mots)

        vocabulaire_dict = {mot: indice for indice, mot in enumerate(vocabulaire_set)}
    
        return vocabulaire_dict
    
    def freq_vocabulaire(self) :
        if not self.texte_intégral:
            self.texte_intégral = self.concatenate()
        
        vocabulaire = self.construire_vocabulaire()
        occurrences = {mot: {'term_frequency': self.texte_intégral.lower().count(mot), 'document_frequency': 0} for mot in vocabulaire}

        for mot in vocabulaire:
            for doc in self.id2doc.values():
                if mot in doc.texte.lower():
                    occurrences[mot]['document_frequency'] += 1

        occurrences_df = pd.DataFrame({
            'Mot': list(occurrences.keys()),
            'Nombre Occurrences': [item['term_frequency'] for item in occurrences.values()],
            'Nombre Documents': [item['document_frequency'] for item in occurrences.values()]
        })

        return occurrences_df

def nettoyer_texte(texte) :
    texte = texte.lower()
    texte = texte.replace('\n', ' ')
    texte = re.sub(r'[^a-z àáâäèéêëìíîïòóôöùúûüç]', '', texte)
    #texte = re.sub(r'[^\w\s]', '', texte)

    return texte

