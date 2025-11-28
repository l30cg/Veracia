from django.urls import URLPattern, path
from typing import List
from .views import index, analyzer, about

app_name:str = "core"
urlpatterns:List[URLPattern] = [
   path("", index, name="index"),
   path("analyzer/", analyzer, name="analyzer"),
   path("about/", about, name="about")
]
