from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .functions.google_api_bm25 import generar_informacion



def index(request:HttpRequest) -> HttpResponse:
   text = ""
   noticia_buscada = ""
   resultado = ""
   noticias  = []  

   if request.method == "POST":
      if "analyze" in request.POST:
         text = request.POST.get("text")
         if text:
            print('text =', text)
            resultado = generar_informacion(text)
            pre_noticias = resultado["noticias"]
            for n in pre_noticias:
               elem = {
                  'index': len(noticias),
                  'name': 'Noticia ' + str(len(noticias)+1),
                  'title': str(n.noticia().getTitulo()),
                  'body': str(n.html()),
                  'url': str(n.noticia().getURL()),
                  'cantidad_patrones': len(n.patrones()),
                  'veredicto': 'Confirmación'
               }
               for p in n.patrones():
                  if p.es_contradiccion():
                     elem['veredicto'] = 'Contradicción'
                     break
               noticias.append(elem)
            noticia_buscada = resultado["noticia_buscada"]

   return render(request, "core/index.html", {
      "noticias": noticias,
      "noticia_buscada": noticia_buscada,
      "text": text
   })



def analyzer(request:HttpRequest) -> HttpResponse:
   return render(request, "core/analyzer.html")



def about(request:HttpRequest) -> HttpResponse:
   return render(request, "core/about.html")