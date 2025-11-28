class UrlEncoding:
   def join(self, list, word):
      result = "+".join(str(x) for x in list)
      return result + "%22+OR+%22" + word

class UrlEncodingWithAnd:
   def join(self, list, word):
      result = "&".join(str(x) for x in list)
      return result

class UrlEncodingWithSpace:
   def join(self, list, word):
      result = " ".join(str(x) for x in list)
      return result
