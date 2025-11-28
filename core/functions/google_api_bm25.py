import requests
import json
from .noticia import Noticia
from bs4 import BeautifulSoup# Para hacer html parsing
from .bm25_metric import Bm25
import socket
from inscriptis import get_text
from .escaner import Escaner
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
dirname, scriptname = os.path.split(os.path.abspath(__file__))
THIS_DIRECTORY = f'{dirname}{os.sep}'
HEADLESS = False
DRIVER = None


socket.getaddrinfo("localhost", 8080)
Fuentes = [
   "https://factual.afp.com",
   "https://medlineplus.gov",
   # "https://pubmed.ncbi.nlm.nih.gov",
   "https://salud.nih.gov",
   # "https://www.newtral.es",
   # "https://maldita.es",
   "https://www.univsion.com",
]


def load_page(url):
   '''Load the specified page with an automated browser'''
   global DRIVER
   if DRIVER is None:
      service = Service(executable_path=f'{THIS_DIRECTORY}chromedriver.exe')
      options = webdriver.ChromeOptions()
      options.headless = HEADLESS
      options.add_experimental_option('excludeSwitches', ['enable-automation'])
      options.add_experimental_option('excludeSwitches', ['enable-logging'])
      options.add_experimental_option('useAutomationExtension', False)
      DRIVER = webdriver.Chrome(options=options, service=service)
   DRIVER.get(url)


class CustomSearch:
   def __init__(self):
      # Establecer credenciales y url de la API
      self.api_key = "..."
      self.id_buscador = "..."
      self.url = "https://www.googleapis.com/customsearch/v1"
      self.titulo = ""
      self.fuente = ""


   def set_query(self, query):
      self.titulo = query


   def set_fuente(self, fuente):
      self.fuente = fuente


   def get_titulo_y_fuente(self):
      return self.titulo + "+" + self.fuente


   def peticion_inicial(self):
      urls = []
      resultados = requests.get(
         self.url,
         params={
            "key": self.api_key,
            "cx": self.id_buscador,
            "lr": "lang_es",
            "num": 5,
            "q": self.get_titulo_y_fuente(),
         },
      )
      Json = json.loads(resultados.content)

      if 'items' in Json:
         items = Json["items"]
         for item in items:
            urls.append((item["title"], item["link"]))
         return urls
      
      return []


   def obtener_noticias_completas(self, duplas):
      resultados = []
      for info in duplas:
         load_page(info[1])
         html    = DRIVER.page_source
         soup    = BeautifulSoup(html, "html.parser")# Para obtener el titulo de la noticia
         texto   = get_text(html)
         titulo  = info[0] if info[0].find('...') == -1 or soup.title is None else soup.title.string
         noticia = Noticia(titulo, texto)
         noticia.setURL(info[1])
         resultados.append(noticia)
      return resultados


   def realizar_busqueda(self):
      url_set = self.peticion_inicial()
      return self.obtener_noticias_completas(url_set)


def crear_log_noticias(results):
   file = open(
      "results_bm25.txt", "w", encoding="utf-8"
   )  # Abriendo o creando archivo para escribir

   try:
      for j in range(len(Fuentes)):
         file.write(Fuentes[j] + '\n')
         for i in results[j]:
            titulo = ''
            if isinstance(i.getTitulo(), str):
               titulo = i.getTitulo()
            else:
               print('TITULO NO ES STRING:', i.getTitulo())
            file.write(
               titulo
            )  # Escribiendo el título utilizando un parser de html
            file.write("\n")
            file.write(str(i.getRelevancia()))
            file.write("\n")
            pretexto = i.getCuerpo()
            for parrafo in pretexto.split(".\n"):
               cont = len(parrafo)
               dim = 75
               oraciones = parrafo.split("\n")
               for oracion in oraciones:
                  # file.write(oracion+'*\n')
                  while len(oracion) > dim:
                     file.write(oracion[0:dim] + "\n")
                     oracion = oracion[dim:]
                     if len(oracion) == 0:
                        continue
                  file.write(oracion[::] + ".\n")
               file.write("\n")

            file.write(str(i.getURL()))
            file.write(
               "\n#####################################################################################"
            )
            file.write("\n")
   except NameError:
      print(NameError)
   file.close()  # Cerrando el archivo


def obtener_noticias(buscador, titulo):
   resultados = []
   buscador.set_query(titulo)
   for fuente in Fuentes:
      buscador.set_fuente(fuente)
      busqueda = buscador.realizar_busqueda()
      resultados.append(busqueda)
   return resultados


def generar_informacion(user_input):# Titulo
   '''Genera la informacion a partir del titulo, y la guarda en un archivo de texto'''

   search = CustomSearch()
   bm25   = Bm25()

   # Obtener query hasta el primer punto de la primer linea
   user_input = user_input.split('.')[0]
   user_input = user_input.split("\n")[0]

   # Convertir todo a minusculas
   titulo = user_input.lower()

   print('Título en minúsculas:', titulo)

   # Obtener en formato de string el arbol del patron de la query
   patrones_noticia_buscada = Escaner.obtener_patrones(titulo)

   print('TEXTO LEMATIZADO:')
   for i in Escaner.tokenizar(titulo):
      print(i.lema())

   if patrones_noticia_buscada == False:
      return { "noticias": [], "noticia_buscada": user_input }
   
   print('PATRONES ECONTRADOS EN LA QUERY:', len(patrones_noticia_buscada))
   for p in patrones_noticia_buscada:
      p.imprimir()
      print('-------------------------------------------------------------------------\n')

   # Obtener noticias mediante la API de GoogleSearch
   pre_resultados = obtener_noticias(search, titulo)

   # Guardar todas las noticias (sin ordenar) obtenidas por la API en results_bm25.txt
   crear_log_noticias(pre_resultados)

   # Unir resultados en un solo arreglo
   resultados = []
   for x in pre_resultados:
      resultados += x

   # Obtener la relevancia de cada noticia
   bm25.setQuery(titulo)
   bm25.setDocs(resultados)
   noticias_ordenadas = bm25.apply()

   # Generar lista de los patrones encontrados en cada título de noticia
   noticias = []
   for n in noticias_ordenadas:
      if len(n.getCuerpo()) <= 1000000:#! [E088] Text of length X exceeds maximum of 1000000
         print(str(n.getTitulo()))
         e = Escaner(n)
         i = len(patrones_noticia_buscada) - 1
         while i > -1:
            e.escanear(patrones_noticia_buscada[i], False)
            if len(e.patrones()) != 0:
               noticias.append(e)
               break
            i -= 1

   return {
      "noticias": noticias,
      "noticia_buscada": user_input
   }