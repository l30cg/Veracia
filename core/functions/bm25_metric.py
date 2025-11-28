# import numpy as np
from rank_bm25 import BM25Okapi
# from fastbm25 import fastbm25
# from retriv import SparseRetriever


# class Bm25:
#    def __init__(self):
#       self.docs = []
#       self.query = []
#       self.news = []
#       self.result = []


#    def setQuery(self, query):
#       self.query = query


#    def setDocs(self, noticias):
#       self.news = list(set(noticias))  # removiendo duplicados
#       self.docs = [n.getCuerpo() for n in self.news]


#    def apply(self):
#       tmp = self.news
#       sr = SparseRetriever(
#         index_name="new-index",
#         model="bm25",
#         min_df=1,
#         tokenizer="whitespace",
#         stemmer="spanish",
#         stopwords="spanish",
#         do_lowercasing=True,
#         do_ampersand_normalization=True,
#         do_special_chars_normalization=True,
#         do_acronyms_normalization=True,
#         do_punctuation_removal=True,
#       )
#       docs = []
#       for i in range(len(self.docs)):
#          docs.append({'id': 'doc_' + str(i + 1), 'text': self.docs[i]})

#       # print('DOCS SIZE =', len(docs))

#       sr.index(docs)
#       bm25_tmp = sr.search(query=self.query, return_docs=True, cutoff=100)

#       # print('bm25_tmp (SIZE: ',len(bm25_tmp), ') = ', bm25_tmp)

#       doc_scores = [n['score'] for n in bm25_tmp]

#       # print('doc_scores (SIZE: ',len(doc_scores), ') = ', doc_scores)

#       noticias_relevantes = []
#       for i in range(len(doc_scores)):
#          if doc_scores[i] > 0:
#             tmp[i].setRelevancia(doc_scores[i])
#             noticias_relevantes.append(tmp[i])
#       self.result = sorted(set(noticias_relevantes), key=lambda x: x.getRelevancia(), reverse = True)

#       print('\n\nlen(self.result) =', len(noticias_relevantes))
#       for n in self.result:
#          print('RELEVANCIA(', n.getRelevancia(), ',', n.getTitulo(), ',', n.getURL(), ')')
#       print('\n\n')

#       return self.result










# class Bm25:
#    def __init__(self):
#       self.tokenized_corpus = []
#       self.docs = []
#       self.query = []
#       self.news = []
#       self.result = []


#    def setQuery(self, query):
#       self.query = query.split(" ")


#    def setDocs(self, noticias):
#       # self.docs = []
#       # self.tokenized_corpus = []

#       noticias = set(noticias) # removiendo duplicados
#       for n in noticias:
#          self.tokenized_corpus.append(n.getCuerpo().split(" "))
#          self.docs.append(n.getCuerpo())
#       self.news = noticias


#    def apply(self):
#       tmp = list(self.news)
#       noticias_relevantes = []
#       bm25 = fastbm25(self.tokenized_corpus)
#       bm25_tmp = bm25.top_k_sentence(self.query, k=len(self.tokenized_corpus))
#       doc_scores = [n[2] for n in bm25_tmp]

#       # print('doc_scores (SIZE: ',len(doc_scores), ') = ', doc_scores)

#       for i in range(len(doc_scores)):
#          if doc_scores[i] > 0:
#             tmp[i].setRelevancia(doc_scores[i])
#             noticias_relevantes.append(tmp[i])
#       self.result = sorted(set(noticias_relevantes), key=lambda x: x.getRelevancia(), reverse = True)
      
#       print('\n\nlen(self.result) =', len(noticias_relevantes))
#       for n in self.result:
#          print('RELEVANCIA(', n.getRelevancia(), ',', n.getTitulo(), ',', n.getURL(), ')')
#       print('\n\n')

#       return self.result












class Bm25:
   def __init__(self):
      self.tokenized_corpus = []
      self.N = 0
      self.avgdl = 0
      self.docs = []
      self.query = []
      self.news = []
      self.result = []


   def setQuery(self, query):
      self.query = query.split(" ")


   def setDocs(self, noticias):
      self.docs = []
      self.tokenized_corpus = []
      noticias = set(noticias) # removiendo duplicados
      for n in noticias:
         self.tokenized_corpus.append(n.getCuerpo().split(" "))
         self.docs.append(n.getCuerpo())
      self.news = noticias


   def apply(self):
      tmp = list(self.news)
      noticias_relevantes = []
      self.N = len(self.docs)
      self.avgdl = sum(len(doc) for doc in self.docs) / self.N
      bm25 = BM25Okapi(self.tokenized_corpus)
      doc_scores = bm25.get_scores(self.query)

      print('doc_scores (SIZE: ',len(doc_scores), ') = ', doc_scores)

      for i in range(len(doc_scores)):
         if doc_scores[i] > 0:
            tmp[i].setRelevancia(doc_scores[i])
            noticias_relevantes.append(tmp[i])
      self.result = sorted(set(noticias_relevantes), key=lambda x: x.getRelevancia(), reverse = True)

      print('\n\nlen(self.result) =', len(noticias_relevantes))
      for n in self.result:
         print('RELEVANCIA(', n.getRelevancia(), ',', n.getTitulo(), ',', n.getURL(), ')')
      print('\n\n')

      return self.result












# class Bm25:
#    def __init__(self):
#       self.N = 0
#       self.avgdl = 0
#       self.docs = []
#       self.vocab = []
#       self.news = []
#       self.result = []


#    def setDocs(self, noticias):
#       noticias = set(noticias) # removiendo duplicados
#       for n in noticias:
#          self.docs.append(n.getCuerpo())
#       self.news = noticias


#    def setQuery(self, vocab):
#       self.vocab = vocab


#    def init(self):
#       self.N = len(self.docs)
#       self.avgdl = sum(len(sentence) for sentence in self.docs) / self.N


#    def calculate(self, word, sentence, k=1, b=0.75):
#       #term frequency
#       freq = sentence.count(word)  # or f(q,D) - freq of query in Doc
#       tf = (freq * (k + 1)) / (freq + k * (1 - b + b * len(sentence) / self.avgdl))

#       # inverse document frequency...
#       N_q = sum([1 for doc in self.docs if word in doc])  # number of docs that contain the word
#       idf = np.log(((self.N - N_q + 0.5) / (N_q + 0.5)) + 1)
#       return round(tf*idf, 4)


#    def getResult(self):
#       return self.result


#    def apply(self):
#       self.init()
#       noticias_relevantes = []
      
#       # CÓDIGO MODIFICADO
#       for doc in self.news:
#          relevancia = 0.0
#          for word in self.vocab:
#             relevancia = relevancia + self.calculate( word, doc.getCuerpo() )
#          if relevancia > 0:
#             doc.setRelevancia(relevancia)
#             noticias_relevantes.append(doc)

#       self.result = sorted(set(noticias_relevantes), key=lambda x: x.getRelevancia(), reverse = True)

#       print('\n\nlen(self.result) =', len(noticias_relevantes))
#       for n in self.result:
#          print('RELEVANCIA(', n.getRelevancia(), ',', n.getTitulo(), ',', n.getURL(), ')')
#       print('\n\n')

#       return self.result