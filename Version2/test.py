import unittest
from corpus import Corpus
from document import RedditDocument
import pandas as pd

# =============== Test de la classe Corpus ===============
class TestCorpus(unittest.TestCase):

    def test_concatenate(self):
        # Création d'une instance de Corpus
        corpus = Corpus("Test Corpus")

        # Ajout de documents
        doc1 = RedditDocument("Titre1", "Auteur1", "2024/01/01", "url1", "Texte1")
        doc2 = RedditDocument("Titre2", "Auteur2", "2024/01/02", "url2", "Texte2")
        doc3 = RedditDocument("Titre3", "Auteur3", "2024/01/03", "url3", "Texte3")

        corpus.add(doc1)
        corpus.add(doc2)
        corpus.add(doc3)

        # Appel de la méthode concatenate
        result = corpus.concatenate()

        self.assertIn("Texte1", result)
        self.assertIn("Texte2", result)
        self.assertIn("Texte3", result)
    
    def test_search(self):
        # Création d'une instance de Corpus
        corpus = Corpus("Test Corpus")

        # Ajout de documents
        doc1 = RedditDocument("Titre1", "Auteur1", "2024/01/01", "url1", "Texte1")
        doc2 = RedditDocument("Titre2", "Auteur2", "2024/01/02", "url2", "Texte2")
        doc3 = RedditDocument("Titre3", "Auteur3", "2024/01/03", "url3", "Texte3")

        corpus.add(doc1)
        corpus.add(doc2)
        corpus.add(doc3)

        # Appel de la méthode search avec un mot-clé
        keyword = "Texte2"
        result = corpus.search(keyword)

        self.assertIn(keyword, result)
    
    def test_concorde(self):
        # Création d'une instance de Corpus
        corpus = Corpus("Test Corpus")

        # Ajout de documents
        doc1 = RedditDocument("Titre1", "Auteur1", "2024/01/01", "url1", "Texte1")
        doc2 = RedditDocument("Titre2", "Auteur2", "2024/01/02", "url2", "Texte2")
        doc3 = RedditDocument("Titre3", "Auteur3", "2024/01/03", "url3", "Texte3")

        corpus.add(doc1)
        corpus.add(doc2)
        corpus.add(doc3)

        # Appel de la méthode concorde avec un mot-clé
        keyword = "Texte2"
        result = corpus.concorde(keyword, context_size=20)

        self.assertIn(keyword, result['motif trouve'].values)
    
    def test_construire_vocabulaire(self):
        # Création d'une instance de Corpus
        corpus= Corpus("Test Corpus")

        # Ajout de documents
        doc1 = RedditDocument("Titre1", "Auteur1", "2024/01/01", "url1", "Texte1")
        doc2 = RedditDocument("Titre2", "Auteur2", "2024/01/02", "url2", "Texte2")
        doc3 = RedditDocument("Titre3", "Auteur3", "2024/01/03", "url3", "Texte3")

        corpus.add(doc1)
        corpus.add(doc2)
        corpus.add(doc3)

        # Appel de la méthode construire_vocabulaire
        vocabulaire_dict = corpus.construire_vocabulaire()

        self.assertIsInstance(vocabulaire_dict, dict)
        self.assertTrue(len(vocabulaire_dict) > 0)
    
    def test_freq_vocabulaire(self):
        # Création d'une instance de Corpus
        corpus = Corpus("Test Corpus")

        # Ajout de documents
        doc1 = RedditDocument("Titre1", "Auteur1", "2024/01/01", "url1", "Texte1")
        doc2 = RedditDocument("Titre2", "Auteur2", "2024/01/02", "url2", "Texte2")
        doc3 = RedditDocument("Titre3", "Auteur3", "2024/01/03", "url3", "Texte3")

        corpus.add(doc1)
        corpus.add(doc2)
        corpus.add(doc3)

        # Appel de la méthode freq_vocabulaire
        freq_vocabulaire_result = corpus.freq_vocabulaire()

        self.assertIsInstance(freq_vocabulaire_result, pd.DataFrame)
        self.assertTrue(len(freq_vocabulaire_result) > 0)  
        self.assertIn('Mot', freq_vocabulaire_result.columns)  
        self.assertIn('Nombre Occurrences', freq_vocabulaire_result.columns)  
        self.assertIn('Nombre Documents', freq_vocabulaire_result.columns)
    
    def test_recherche(self):
        # Création d'une instance de Corpus
        corpus = Corpus("Test Corpus")

        # Ajout de documents
        doc1 = RedditDocument("Titre1", "Auteur1", "2024/01/01", "url1", "Texte1")
        doc2 = RedditDocument("Titre2", "Auteur2", "2024/01/02", "url2", "Texte2")
        doc3 = RedditDocument("Titre3", "Auteur3", "2024/01/03", "url3", "Texte3")

        corpus.add(doc1)
        corpus.add(doc2)
        corpus.add(doc3)

        # Appel de la méthode recherche avec une requête
        query = "Texte2"
        resultats_recherche = corpus.recherche(query)

        self.assertIsInstance(resultats_recherche, dict)  
        self.assertTrue(len(resultats_recherche) == len(corpus.id2doc)) 

if __name__ == '__main__':
    unittest.main()