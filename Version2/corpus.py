from author import *
from document import *
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import re
import pandas as pd
import scipy
import numpy as np

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
        self.vocab = {}
 
    
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
    
    def nettoyer_texte(self, texte) :
        texte = str(texte).lower()
        texte = texte.replace('\n', ' ')
        texte = re.sub(r'[^a-z àáâäèéêëìíîïòóôöùúûüç]', '', texte)
        #texte = re.sub(r'[^\w\s]', '', texte)
        return texte
        

    def construire_vocabulaire(self):
        if not self.texte_intégral:
            self.texte_intégral = self.concatenate()

        for doc in self.id2doc.values():
            texte_doc_nettoye = self.nettoyer_texte(doc.texte)
            # print(texte_doc_nettoye)
            mots = texte_doc_nettoye.split()
            self.vocabulaire.update(mots)

        vocabulaire_dict = {mot: indice for indice, mot in enumerate(self.vocabulaire)}
    
        return vocabulaire_dict

    # def construire_vocab(self):
    #     if not self.texte_intégral:
    #         self.texte_intégral = self.concatenate()
    #     mots = self.texte_intégral.split()
    #     self.vocab = {mot: {'id': i, 'occurrences': 0} for i, mot in enumerate(sorted(set(mots)))}

    #     for mot in mots:
    #         self.vocab[mot]['occurrences'] += 1 
    #     return self.vocab

    
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
    
    def mat_TF(self):
        matrice = scipy.sparse.csr_matrix((self.ndoc + 1, len(self.vocabulaire)), dtype=np.intc)
        for i, document in self.id2doc.items():
            texte_doc_nettoye = self.nettoyer_texte(document.texte)
            mots = texte_doc_nettoye.split()
            mots_non_trouves = set()
            for mot in mots:
                if mot not in self.vocabulaire:
                    print(f'Mot non trouvé dans le vocabulaire : {mot}')
                    mots_non_trouves.add(mot)
                else:
                    j = list(self.vocabulaire).index(mot)
                    matrice[i, j] += 1
            if mots_non_trouves:
                print(f'Mots non trouvés dans le vocabulaire : {mots_non_trouves}')
        return matrice
    
    # def update_vocab(self):
    #     matrice_TF = self.mat_TF()
    #     for mot, info in self.vocab.items():
    #         indice_mot = info['id']
    #         documents_contenant = (matrice_TF[:, indice_mot] > 0).sum()
    #         self.vocab[mot]['documents_contenant'] = documents_contenant

    #     return self.vocab

    def construire_vocab(self):
        matrice_TF = self.mat_TF()
        self.vocab = {mot: {'id': i, 'Nombre Total Occurrences': 0, 'Nombre Total Documents': 0} for i, mot in enumerate(self.vocabulaire)}

        for i, document in self.id2doc.items():
            mots = self.nettoyer_texte(document.texte).split()
            mots_non_trouves = set()

            for mot in mots:
                if mot in self.vocabulaire:
                    j = list(self.vocabulaire).index(mot)
                    self.vocab[mot]['Nombre Total Occurrences'] += matrice_TF[i, j]
                    if matrice_TF[i, j] > 0:
                        self.vocab[mot]['Nombre Total Documents'] += 1
                else:
                    mots_non_trouves.add(mot)

            if mots_non_trouves:
                print(f'Mots non trouvés dans le vocabulaire : {mots_non_trouves}')

        return self.vocab


    # def mat_tfIdf(self):
    #     vectorizer = TfidfVectorizer()
    #     for i, document in self.id2doc.items():
    #         texte_doc_nettoye = self.nettoyer_texte(document.texte)
    #         mots = texte_doc_nettoye.split()

    def mat_TFxIDF(self):
        mat_TF = self.mat_TF()
        nb_docs_contenant_terme = np.sum(mat_TF > 0, axis=0)
        nb_docs_total = self.ndoc + 1

        idf = np.log(nb_docs_total / (nb_docs_contenant_terme + 1))

        mat_TFxIDF = mat_TF.multiply(idf)

        return mat_TFxIDF
    
    def recherche(self, query):
        
        #recuperer mots clés
        req_nettoye = self.nettoyer_texte(query)
        mots_cle = req_nettoye.split()
    
        #vectoriser les mots clés
        vecteur_req =[1 if mot in mots_cle else 0 for mot in self.vocabulaire]

        #calculer similarité
        res = {}
        for i, document in self.id2doc.items():
            mots = self.nettoyer_texte(document.texte).split()
            vecteur_doc = [1 if mot in mots else 0 for mot in self.vocabulaire]
            similarite = np.dot(vecteur_req, vecteur_doc)
            res[i] = similarite
        
        #trier score
        res_sorted = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
        return res_sorted
    
    def afficher(self, res):
        for resultat in res.items():
            index_doc = resultat[0]
            doc = self.id2doc[index_doc]
            print(f"Document: {doc.titre}")
            print(f"Date: {doc.date}")
            print(f"Source: {doc.type}")
            print(f"Contenu: {doc.texte}")
            print("=" * 50)  # Ajoute une ligne de séparation pour une meilleure lisibilité
        

        





