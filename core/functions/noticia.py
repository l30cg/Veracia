# Clase para almacenar la información de la noticia
class Noticia:
   def __init__(self, titulo, cuerpo):
      self.titulo = titulo
      self.cuerpo = cuerpo
      self.relevancia = 0
      self.url = ''

   def __eq__(self, other):
      return self.titulo==other.titulo

   def __hash__(self):
      return hash(('titulo', self.titulo))

   def setRelevancia(self, relevancia):
      self.relevancia = relevancia

   def getTitulo(self):
      return self.titulo

   def getCuerpo(self):
      return self.cuerpo

   def setURL(self, url):
      self.url = url

   def setCuerpo(self, cuerpo):
      if type(cuerpo) is list:
         cuerpo = " ".join(cuerpo)
      self.cuerpo = cuerpo

   def getRelevancia(self):
      return self.relevancia

   def getURL(self):
      return self.url