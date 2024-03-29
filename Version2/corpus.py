from author import *
from document import *
# from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import re
import pandas as pd
import scipy
import numpy as np
import os
# from IPython.display import HTML

# Fonction décoratrice pour créer un singleton
# def singleton(cls):
#     instance =[None]
#     def wrapper(*args,**kwargs):
#         nonlocal instance
#         if instance[0] is None:
#             instance[0] = cls(*args,**kwargs)
#         return instance[0]
#     return wrapper

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
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'wb') as f:
            pickle.dump(self, f)

    # Charge le corpus à partir d'un fichier binaire
    @classmethod
    def load(cls, file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f) 
    
    # Utilisation de la fonction join pour concaténer le texte de tous les documents
    def concatenate(self):
        return " ".join([doc.texte for doc in self.id2doc.values()])

    def search(self, keyword):
        if not self.texte_intégral :
            self.texte_intégral = self.concatenate()
        
        # Utilisation de re.finditer pour trouver toutes les occurrences du mot-clé dans le texte intégral
        matches = re.finditer(keyword, self.texte_intégral, re.IGNORECASE)
       
        # Création d'une liste de passages en utilisant set pour éliminer les doublons
        passages = list(set(match.group() for match in matches))

        return passages
    
    # Fonction recherchant et extrayant les concordances d'un mot-clé dans le texte intégral du corpus avec un contexte spécifié
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
    
    # Fonction qui convertit le texte en minuscules, remplace les sauts de ligne par des espaces, et élimine les caractères non alphabétiques
    def nettoyer_texte(self, texte) :
        texte = str(texte).lower()
        texte = texte.replace('\n', ' ')
        texte = re.sub(r'[^a-z àáâäèéêëìíîïòóôöùúûüç]', '', texte)

        return texte

    # Construit un dictionnaire de vocabulaire à partir du texte intégral du corpus en nettoyant les documents et en extrayant les mots
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
    
    # Calcule la fréquence d'occurrence et le nombre de documents pour chaque mot dans le texte intégral du corpus
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
    
    # Fonction qui construit et retourne une matrice de termes-fréquence (TF) à partir du texte intégral du corpus, en utilisant une représentation sparse (CSR)
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
    
    # Construit et retourne un dictionnaire de vocabulaire étendu à partir de la matrice de termes-fréquence (TF) du corpus
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
    
    # Calcule et retourne une matrice de termes-fréquence * inverse du document (TFxIDF) en utilisant la matrice de termes-fréquence (TF) du corpus
    def mat_TFxIDF(self):
        mat_TF = self.mat_TF()
        nb_docs_contenant_terme = np.sum(mat_TF > 0, axis=0)
        nb_docs_total = self.ndoc + 1

        idf = np.log(nb_docs_total / (nb_docs_contenant_terme + 1))

        mat_TFxIDF = mat_TF.multiply(idf)

        return mat_TFxIDF
    
    # Recherche et classe les documents par similarité avec la requête
    def recherche(self, query):
        
        # Récupérer les mots clés
        req_nettoye = self.nettoyer_texte(query)
        mots_cle = req_nettoye.split()
        
        # Vectoriser les mots clés
        vecteur_req =[1 if mot in mots_cle else 0 for mot in self.vocabulaire]

        # Calculer la similarité
        res = {}
        mat_tfidf = self.mat_TFxIDF()
        liste_vocabulaire = list(self.vocabulaire)
        mat_tfidf_csr = mat_tfidf.tocsr()
        for i, document in self.id2doc.items():
            mots = self.nettoyer_texte(document.texte).split()
            indices_mot = [liste_vocabulaire.index(mot) for mot in mots if mot in liste_vocabulaire]
            valeurs_tfidf = [mat_tfidf_csr[i, indice] for indice in indices_mot]
            vecteur_doc = [0] * len(liste_vocabulaire)
            for indice_mot, valeur_tfidf in zip(indices_mot, valeurs_tfidf):
                vecteur_doc[indice_mot] = valeur_tfidf
            similarite = np.dot(vecteur_req, vecteur_doc)
            res[i] = similarite
        
        # Trier les scores de similarité
        res_sorted = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
        return res_sorted
    
    # Génère une représentation HTML des résultats de recherche avec les détails de chaque document
    def afficher(self, res):
        html_output = ""
        for resultat in res.items():
            index_doc = resultat[0]
            doc = self.id2doc[index_doc]
            html_output += f"<p><b>Document:</b> {doc.titre}</p>"
            html_output += f"<p><b>Date:</b> {doc.date}</p>"
            html_output += f"<p><b>Source:</b> {doc.type}</p>"
            html_output += f"<p><b>Contenu:</b> {doc.texte}</p>"
            html_output += "=" * 50 + "<br><br>"
        return html_output  

