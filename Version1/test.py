import unittest
import io
import pickle
from unittest.mock import patch
from corpus import Corpus
from document import RedditDocument

# =============== Test de la classe Corpus ===============
class TestCorpus(unittest.TestCase):
    def test_showDate(self):
        # Création d'une instance de Corpus pour le test
        corpus = Corpus("Test Corpus")

        # Ajout de RedditDocuments de test au Corpus avec des dates différentes
        doc1 = RedditDocument("Titre1", "Auteur1", "2022/01/01", "url1", "Texte1")
        doc2 = RedditDocument("Titre2", "Auteur2", "2022/01/02", "url2", "Texte2")
        doc3 = RedditDocument("Titre3", "Auteur3", "2022/01/03", "url3", "Texte3")

        corpus.id2doc = {0: doc1, 1: doc2, 2: doc3}

        # Redirection de la sortie standard pour capturer les résultats imprimés
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            # Appel de la méthode showDate
            corpus.showDate(2)

            # Récupération de la sortie imprimée
            output = mock_stdout.getvalue()

        # Assertions basées sur la sortie attendue
        self.assertIn("Date: 2022/01/01", output)
        self.assertIn("Date: 2022/01/02", output)
        self.assertNotIn("Date: 2022/01/03", output)

    def test_showTitre(self):
        # Création d'une instance de Corpus pour le test
        corpus = Corpus("Test Corpus")

        # Ajout de RedditDocuments de test au Corpus avec des titres différents
        doc1 = RedditDocument("TitreC", "Auteur1", "2022/01/01", "url1", "Texte1")
        doc2 = RedditDocument("TitreB", "Auteur2", "2022/01/02", "url2", "Texte2")
        doc3 = RedditDocument("TitreA", "Auteur3", "2022/01/03", "url3", "Texte3")

        corpus.id2doc = {0: doc1, 1: doc2, 2: doc3}

        # Redirection de la sortie standard pour capturer les résultats imprimés
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            # Appel de la méthode showTitre
            corpus.showTitre(2)

            # Récupération de la sortie imprimée
            output = mock_stdout.getvalue()

        # Assertions basées sur la sortie attendue
        self.assertIn("Titre: TitreA", output)
        self.assertIn("Titre: TitreB", output)
        self.assertNotIn("Titre: TitreC", output)

    def test_add(self):
        # Création d'une instance de Corpus pour le test
        corpus = Corpus("Test Corpus")

        # Création d'un document de test
        doc = RedditDocument("Titre1", "Auteur1", "2022/01/01", "url1", "Texte1")

        # Appel de la méthode add pour ajouter le document au corpus
        corpus.add(doc)

        # Assertions basées sur l'état attendu du corpus après l'ajout
        self.assertEqual(corpus.naut, 1)  # Un auteur doit être ajouté
        self.assertEqual(corpus.ndoc, 1)  # Un document doit être ajouté
        self.assertIn(doc.titre, [d.titre for d in corpus.id2doc.values()])  # Le document doit être dans id2doc
        self.assertIn(doc.auteur, corpus.aut2id.keys())  # L'auteur doit être dans aut2id

        # Vérification de l'ajout correct de l'auteur
        author_id = corpus.aut2id[doc.auteur]
        self.assertEqual(corpus.authors[author_id].name, doc.auteur)  # Le nom de l'auteur doit correspondre
        self.assertEqual(corpus.authors[author_id].production, [doc.texte])  # Le texte du document doit être ajouté à l'auteur

    def test_repr(self):
        # Création d'une instance de Corpus pour le test
        corpus = Corpus("Test Corpus")

        # Ajout d'un document pour avoir quelque chose à représenter
        doc = RedditDocument("Titre1", "Auteur1", "2022/01/01", "url1", "Texte1")
        corpus.add(doc)

        # Appel de la méthode __repr__
        repr_result = repr(corpus)

        # Assertions basées sur le format réel de votre méthode __repr__
        self.assertIn("Titre1, par Auteur1, Source: Reddit\nNombre de commentaires : 0", repr_result)

    def test_save(self):
        # Création d'une instance de Corpus pour le test
        corpus = Corpus("Test Corpus")

        # Ajout d'un document pour avoir quelque chose à sauvegarder
        doc = RedditDocument("Titre1", "Auteur1", "2022/01/01", "url1", "Texte1")
        corpus.add(doc)

        # Sauvegarde du corpus dans un fichier binaire
        file_path = "test_corpus.pkl"
        corpus.save(file_path)

        # Chargement du corpus depuis le fichier
        with open(file_path, 'rb') as f:
            loaded_corpus = pickle.load(f)

        # Assertions basées sur le corpus chargé depuis le fichier
        self.assertEqual(len(loaded_corpus.id2doc), 1)
        self.assertEqual(loaded_corpus.id2doc[1].titre, "Titre1")
       
    def test_load(self):
        # Création d'une instance de Corpus pour le test
        corpus = Corpus("Test Corpus")

        # Ajout d'un document pour avoir quelque chose à sauvegarder
        doc = RedditDocument("Titre1", "Auteur1", "2022/01/01", "url1", "Texte1")
        corpus.add(doc)

        # Sauvegarde du corpus dans un fichier binaire
        file_path = "test_corpus.pkl"
        corpus.save(file_path)

        # Chargement du corpus depuis le fichier
        loaded_corpus = Corpus.load(file_path)

        # Assertions basées sur le corpus chargé depuis le fichier
        self.assertEqual(len(loaded_corpus.id2doc), 1)
        self.assertEqual(loaded_corpus.id2doc[1].titre, "Titre1")

if __name__ == '__main__':
    unittest.main()