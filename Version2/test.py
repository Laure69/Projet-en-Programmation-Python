import unittest
from corpus import Corpus
from document import RedditDocument

class TestCorpusConcatenateMethod(unittest.TestCase):

    def test_concatenate(self):
        # Création d'une instance de Corpus pour le test
        corpus = Corpus("Test Corpus")

        # Ajout de documents avec différents textes
        doc1 = RedditDocument("Titre1", "Auteur1", "2022/01/01", "url1", "Texte1")
        doc2 = RedditDocument("Titre2", "Auteur2", "2022/01/02", "url2", "Texte2")
        doc3 = RedditDocument("Titre3", "Auteur3", "2022/01/03", "url3", "Texte3")

        corpus.add(doc1)
        corpus.add(doc2)
        corpus.add(doc3)

        # Appel de la méthode concatenate
        result = corpus.concatenate()

        # Assertions
        self.assertIn("Texte1", result)
        self.assertIn("Texte2", result)
        self.assertIn("Texte3", result)
        # Ajoutez d'autres assertions en fonction de votre logique d'application
    
    def test_search(self):
        # Création d'une instance de Corpus pour le test
        corpus = Corpus("Test Corpus")

        # Ajout de documents avec différents textes
        doc1 = RedditDocument("Titre1", "Auteur1", "2022/01/01", "url1", "Texte1")
        doc2 = RedditDocument("Titre2", "Auteur2", "2022/01/02", "url2", "Texte2")
        doc3 = RedditDocument("Titre3", "Auteur3", "2022/01/03", "url3", "Texte3")

        corpus.add(doc1)
        corpus.add(doc2)
        corpus.add(doc3)

        # Appel de la méthode search avec un mot-clé présent dans un des documents
        keyword = "Texte2"
        result = corpus.search(keyword)

        # Assertions
        self.assertIn(keyword, result)
    
    def test_concorde(self):
        # Création d'une instance de Corpus pour le test
        corpus = Corpus("Test Corpus")

        # Ajout de documents avec différents textes
        doc1 = RedditDocument("Titre1", "Auteur1", "2022/01/01", "url1", "Texte1")
        doc2 = RedditDocument("Titre2", "Auteur2", "2022/01/02", "url2", "Texte2")
        doc3 = RedditDocument("Titre3", "Auteur3", "2022/01/03", "url3", "Texte3")

        corpus.add(doc1)
        corpus.add(doc2)
        corpus.add(doc3)

        # Appel de la méthode concorde avec un mot-clé présent dans un des documents
        keyword = "Texte2"
        result = corpus.concorde(keyword, context_size=20)

        # Assertions
        self.assertIn(keyword, result['motif trouve'].values)

if __name__ == '__main__':
    unittest.main()