from .token import Token
from .patron import Patron
import spacy
import nltk
import re

# Clase para buscar patrones gramaticales dentro de una noticia
class Escaner:
   tokenizador = spacy.load("es_core_news_lg")
   # with open("Gramatica.cfg", "r", encoding="utf-8") as f:
   with open("curaciones/core/functions/Gramatica.cfg", "r", encoding="utf-8") as f:
      gramatica = nltk.CFG.fromstring(f.read())


   def tokenizar(texto:str):
      texto = re.sub('(\w{1})([,\.;])', '\g<1> \g<2>', texto)
      texto = re.sub('(&nbsp;)|\(\.\.\.\)|(\[\.\.\.\])', '', texto)
      texto += '\n'
      return [Token(t) for t in Escaner.tokenizador(texto)]
   

   def obtener_patrones(texto:str):
      # Obtiene el primer patrón de solo la primera línea del texto
      tokens = Escaner.tokenizar(texto=texto)
      x = Escaner.__obtener_patrones(tokens=tokens, index=0, fin=len(tokens))
      if x == False or x['patrones'] is None:
          return False
      return x['patrones']


   def __init__(self, noticia):
      self.noticia_  = noticia
      self.tokens_   = None
      self.patrones_ = None
      self.patrones_busqueda_ = []
      self.html_     = None
   

   def __obtener_patrones(tokens, index, fin):
      # Validamos el parámetro index
      if index < 0:
         return False

      # Creamos el parser
      parser = nltk.ChartParser(Escaner.gramatica)

      # Seleccionamos todas las palabras del párrafo palabras que no sean stopwords, la cantidad puede ser configurada según el máximo número de ngramas posibles en un patrón
      palabras = []
      desconocidos = []
      indices = []
      while index < fin:
         if tokens[index].es_fin_parrafo():
            break
         if not tokens[index].es_stopword():
            lema = tokens[index].lema()
            if lema not in Escaner.gramatica._lexical_index:
               desconocidos.append(lema)
            else:
               palabras.append(lema)
               indices.append(tokens[index].index())
         index += 1


      # print('\nPALABRAS:', palabras)
      # print('UNK:', desconocidos)

      # El texto es muy corto para coincidir con un patrón
      if len(palabras) < 3:
         return False
      
      # Retorna una lista de arboles ordenados de mayor semejanza a menor semejanza de los patrones
      # que coinciden con el título de la noticia
      patrones = []
      indices_patrones = []
      while len(palabras) > 2:# Recorrer índice de inicio
         i = 2
         while i < len(palabras):# Ir aumentando número del muestreo
               muestra = palabras[:i + 1]
               i += 1
               resultados = parser.parse(muestra)
               for resultado in resultados:
                  patrones.append(resultado)
                  indices_patrones.append(indices.copy())
                  break
         palabras.pop(0)
         indices.pop(0)

      if len(patrones) > 0:
         patrones_final = []
         for i in range(len(patrones)):
            cantidad_palabras = len(patrones[i].leaves())
            patrones_final.append(Patron(patrones[i][0], indices_patrones[i][0], indices_patrones[i][cantidad_palabras - 1]))
         patrones_final = sorted(patrones_final, key=lambda x: len(x.arbol().leaves()))
         return {'indice': indices_patrones[-1][cantidad_palabras - 1] + 1, 'patrones': patrones_final}
      
      return {'indice': indices[0] + 1, 'patrones': None}
   

   def __desmarcar_tokens(self):
      for t in self.tokens_:
         t.set_es_inicio_patron(False)
         t.set_es_fin_patron(False)
         t.set_es_inicio_relevante(False)
         t.set_es_fin_relevante(False)
   

   def __busqueda_cache(self, query:Patron, modo_estricto=True):# Marca los tokens para distinguir aquellos que contienen un patrón o son una oración relevante que un patrón
      patrones = []
      self.__desmarcar_tokens()
      for p in self.patrones_:
         if p.comparar(query, modo_estricto=modo_estricto) == True:
            print('[TRUE]\n\n')
            patrones.append(p)
            self.tokens_[p.index_inicio()].set_es_inicio_patron(True)
            self.tokens_[p.index_fin()].set_es_fin_patron(True)
            if p.index_fin_parrafo() is not None:
               self.tokens_[p.index_inicio_parrafo()].set_es_inicio_relevante(True)
               self.tokens_[p.index_fin_parrafo()].set_es_fin_relevante(True)
         else:
            print('[FALSE]\n\n')
      self.patrones_busqueda_ = patrones
      return patrones
   

   def escanear(self, query:Patron, modo_estricto=True):# Escanea una sola vez el documento y guarda todos los patrones encontrados (funge como un cache) para agilizar las futuras búsquedas con los patrones ya almacenados de tal modo que solo se requiera comparar los patrones con la query de la búsqueda
      self.html_ = None

      if self.tokens_ is not None and self.patrones_ is not None:
         return self.__busqueda_cache(query=query, modo_estricto=modo_estricto)
      
      self.tokens_ = Escaner.tokenizar(self.noticia_.getCuerpo())
      i = 0
      fin = len(self.tokens_)
      patrones = []
      index_inicio_parrafo = -1
      patron_encontrado = False
      while i < fin:
         if self.tokens_[i].es_inicio_parrafo() or (i > 0 and self.tokens_[i - 1].es_fin_parrafo()):
               index_inicio_parrafo = i
         if self.tokens_[i].es_fin_parrafo():
               if patron_encontrado:
                  patrones[-1].set_index_inicio_parrafo(index_inicio_parrafo)
                  patrones[-1].set_index_fin_parrafo(i-1)
                  patron_encontrado = False
               index_inicio_parrafo = -1
         if not self.tokens_[i].es_stopword():
               x = Escaner.__obtener_patrones(tokens=self.tokens_, index=i, fin=fin)
               if x != False:
                  if x['patrones'] is not None:
                        patrones.append(x['patrones'][-1])# Considera solo el patrón de mayor longitud
                        patron_encontrado = True
                  i = x['indice']# Resumir escaneo desde la posicion en la cual termina el patrón recién encontrado
                  continue
         i += 1
      self.patrones_ = patrones
      return self.__busqueda_cache(query=query, modo_estricto=modo_estricto)
   

   def patrones(self):
      return self.patrones_busqueda_
   

   def noticia(self):
      return self.noticia_
   

   def html(self):
      if self.html_ is not None:
         return self.html_
      
      id_relevante = 0
      id_patron = 0
      html = ''
      for i in range(len(self.tokens_)):
         if self.tokens_[i].es_inicio_relevante():
            html += '<span class=\'relevante\' id=\'patron'+ str(id_relevante) +'\'>'
            id_relevante += 1
         if self.tokens_[i].es_inicio_patron():
            clase = 'patron'
            css_params = '--n:500;'
            if self.patrones_busqueda_[id_patron].es_contradiccion():
               clase += '_contradiccion'
               css_params += ' --cursor: red; --font: rgb(213,35,34);'
            else:
               css_params += ' --cursor: blue; --font: rgb(0,0,153);'
            html += '<span class=\'' + clase + '\' style=\''+ css_params +'\'>'
            id_patron += 1
         t = self.tokens_[i].texto()
         if t not in ['.', ';', ',']:
            html += ' '
         if self.tokens_[i].impl_.is_space:
             for j in range(len(t)):
                  if t[j] == '\n':
                     html += '<br>'
                  elif t[j] == '\t':
                     html += '&emsp;'
                  #elif t[j] == ' ':
                     #html += '&nbsp;'
         html += t
         if self.tokens_[i].es_fin_patron():
            html += '</span>'
         if self.tokens_[i].es_fin_relevante():
            html += '</span>'
      self.html_ = html
      return self.html_