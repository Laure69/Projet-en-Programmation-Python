import praw 
import urllib.request
import xmltodict
from author import *
from document import *
from corpus import Corpus
import datetime

def DocCorpus(query, nbArticle) :
    # Connexion à l'API Reddit
    reddit = praw.Reddit(client_id='BPhj4dO4S48SLnwoyR0BWA', client_secret='GtW2Sp9qyO8NuQBs51KW6T24UJntSg', user_agent='TD3 Python')
    subr = reddit.subreddit(query)

    # Récupération des 100 premiers posts les plus populaires de la subreddit
    hot_post = subr.hot(limit=nbArticle)

    docs = []
    docs_bruts = []

    # Extraire les titres, en remplaçant les sauts de ligne par des espaces
    for post in hot_post:
        texte = post.selftext
        texte = texte.replace("\n", " ")
        if len(texte) >= 20 :
            docs.append(texte)
            docs_bruts.append(('Reddit', post))

    # Requête à l'API d'Arxiv pour récupérer les 100 premiers articles liés à la recherche
    url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results='+str(nbArticle)
    url_read = urllib.request.urlopen(url).read()
    data =  url_read.decode()
    dico = xmltodict.parse(data)
    arxiv = dico['feed']['entry']

    for i, entry in enumerate(arxiv):
        if len(entry["summary"]) >= 20 :
            docs.append(entry["summary"].replace("\n", ""))
            docs_bruts.append(('Arxiv', entry))

    # Concaténation de tous les documents en une seule chaîne de caractères
    longueChaineDeCaracteres = " ".join(docs)

    docRedditArxiv = []

    for origine, doc in docs_bruts :
        # Création d'instances de documents en fonction de leur origine (Reddit ou Arxiv)
        if origine == 'Reddit' :
            titre = doc.title.replace("\n", '')
            auteur = str(doc.author)
            # Formatage de la date en année/mois/jour avec librairie datetime
            date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
            url = "https://www.reddit.com/" + doc.permalink
            texte = doc.selftext.replace("\n", '')

            docReddit = RedditDocument(titre, auteur, date, url, texte)
            docReddit.nbr_com = doc.num_comments

            docRedditArxiv.append(docReddit)

        elif origine == 'Arxiv' :
            titre = doc['title'].replace("\n", '')
            try:
                authors = [a["name"] for a in doc["author"]]
            except:
                authors = doc["author"]["name"] 
            
            summary = doc["summary"].replace("\n", "") 
            
            # Formatage de la date en année/mois/jour avec librairie datetime
            date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")

            docArxiv = ArxivDocument(titre, authors, date, doc['id'], summary)
            docRedditArxiv.append(docArxiv)

    # Création d'un dictionnaire pour représenter les documents par leur titre
    id2doc = {}

    for i, doc in enumerate(docRedditArxiv) :
        # Utilisation de l'identifiant comme clé et l'objet de document comme valeur
        id2doc[i] = doc.titre

    # Création d'un dictionnaire pour représenter les auteurs par leur identifiant
    id2auteur = {}
    idauteur = 0

    for doc in docRedditArxiv :
        if doc.auteur not in id2auteur :
            idauteur += 1
            auteur = Author(doc.auteur)
            id2auteur[idauteur] = auteur
        
        id2auteur[idauteur].add(doc.texte)

    # Création d'une instance de Corpus et ajout des documents
    corpus = Corpus("Mon corpus")

    for doc in docRedditArxiv:
        corpus.add(doc)

    # Sauvegarde du corpus dans un fichier binaire
    corpus.save('Version2/'+query+'.pkl') 
    
DocCorpus("orcas", 10)

# corpuscharger = Corpus("TestCorpus")
# c = corpuscharger.load('./Version2/corpus.pkl')  

# #fonction concorde
# print(c.concorde("france", 25)) 

# #fonction nettoyer_texte
# # exemple_document = c.id2doc[3]
# # print("Texte original du corpus :\n", exemple_document.texte)
# # texte_nettoye = c.nettoyer_texte(exemple_document.texte)
# # print("\nTexte nettoyé du corpus :\n", texte_nettoye)

# # #fonction construire_vocabulaire
# print(c.construire_vocabulaire())

# # #fonction construire_vocab
# print(c.construire_vocab())

# # #fonction freq_vocabulaire
# print(c.freq_vocabulaire())

# # print(c.mat_TF())
# # print(c.update_vocab())

# print(c.mat_TFxIDF())

# print(c.recherche("amour sante"))
# res_recherche = c.recherche("amour sante")
# c.afficher(res_recherche)