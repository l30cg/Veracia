from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

class StopwordFilter:
   def __init__(self, text, encoder):
      self.text = text
      self.stopwords = stopwords.words('spanish')
      self.textFiltered = []
      self.result_list = []
      self.result_string = ""
      self.url_encoder = encoder

   def setLanguage(self, lang):
      self.stopwords = stopwords.words(lang)

   def filter(self):
      words = word_tokenize(self.text)
      for w in words:
         if w not in self.stopwords:
            self.textFiltered.append(w)
      return self.textFiltered

   def join(self, list, word):
      result = "+".join(str(x) for x in list)
      return result + "%22+OR+%22" + word # no insertar aquí

   def setUrlEncoder(self, encoder):
      self.url_encoder = encoder

   def getResult(self):
      l = self.textFiltered
      copy = []
      for i in range(len(l)):
         for j in range(len(l)):
            if l[j] != l[i]:
               copy.append(l[j])
         self.result_list.append(self.url_encoder.join(copy, l[i]))
         copy = []
      return self.result_list

   def printResult(self):
      cad = " ".join(str(x) for x in self.textFiltered)
      print(cad)
      self.result_string = cad

   def getTitle(self):
      return self.text

   def getModQuery(self):
      self.result_list = [self.url_encoder.join( self.textFiltered, "" )]
      return self.result_list

   def printBaseText(self):
      print(self.text)

   def saveToFile(self):
      file = open("log.txt","a")
      file.write(str(self.result_list))
      file.write("\n")
      self.result_string = " ".join(str(x) for x in self.textFiltered)
      file.write(str(self.result_string))
      file.write("\n\n")
      file.close()
