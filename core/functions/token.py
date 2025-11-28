import re

class Token:
   lemas = {
      'uso': 'usar',
      'causado': 'causar',
      'cura': 'curar',
      'postizas': 'postizo',
      'acrílica': 'acrílico',
      'lent': 'lente',
      'calmant': 'calmante',
      'eliminado': 'eliminar',
      'pupilent': 'pupilente',
      'generado': 'generar',
      'mariguán': 'mariguana',
      'ablepsio' : 'ablepsia',
      'provocado': 'provocar',
      'insulín': 'insulina',
      'espermatozoid': 'espermatozoide',
      'hombr': 'hombre',
      'vacunación': 'vacuna',
      'vacunar': 'vacuna',
      'vacunir': 'vacuna',
      'combate': 'combatir',
      'aumento': 'aumentar',
      'sífili': 'sífilis',
      'evidenciar': 'evidencia',
      'hipoacusio': 'hipoacusia',
      'cotonet': 'cotonete',
      'microondas': 'microonda',
      'simvastatín': 'simvastatina',
      'tiroid': 'tiroide',
      'jengibrir': 'jengibre',
      'previnar': 'prevenir',
      'ataques': 'ataque',
   }

   def __init__(self, elem):
       self.index_ = elem.i
       self.texto_ = elem.text
       self.lema_  = elem.lemma_
       self.es_stopword_ = elem.is_stop
       self.impl_  = elem
       self.es_inicio_patron_ = False
       self.es_fin_patron_ = False
       self.es_inicio_relevante_ = False
       self.es_fin_relevante_ = False

   def __str__(self):
       return self.texto_

   def es_stopword(self):
       return re.search('\w|[áéíóúüÁÉÍÓÚÜñÑ]', self.texto_) is None or (self.lema() not in ['no', 'tampoco', 'solo', 'usar', 'haber', 'ser', 'cierto', 'posible'] and self.es_stopword_)

   def index(self):
       return self.index_
   
   def lema(self):
       lema = self.texto_.lower()
       if lema in ['lavanda']:
           return lema
       return self.lema_.lower() if self.lema_ not in Token.lemas else Token.lemas[self.lema_.lower()]

   def texto(self):
       return self.texto_

   def es_inicio_patron(self):
       return self.es_inicio_patron_

   def es_fin_patron(self):
       return self.es_fin_patron_

   def set_es_inicio_patron(self, valor):
       self.es_inicio_patron_ = valor

   def set_es_fin_patron(self, valor):
       self.es_fin_patron_ = valor

   def es_inicio_relevante(self):
       return self.es_inicio_relevante_

   def es_fin_relevante(self):
       return self.es_fin_relevante_

   def set_es_inicio_relevante(self, valor):
       self.es_inicio_relevante_ = valor

   def set_es_fin_relevante(self, valor):
       self.es_fin_relevante_ = valor

   def es_inicio_parrafo(self):
       return self.impl_.is_sent_start

   def es_fin_parrafo(self):
       return self.impl_.is_sent_end or re.search('\n', self.texto()) is not None