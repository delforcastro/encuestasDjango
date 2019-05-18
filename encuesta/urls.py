from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'encuesta'

urlpatterns = [
    #ejemplo: /encuesta/
    path ('', views.VistaIndex.as_view(), name='index'),
    #ejemplo: /encuesta/2/
    path ('<int:pk>/', views.VistaDetalle.as_view(), name='detalle'),
    #ejemplo: /encuesta/2/resultados/
    path ('<int:pk>/resultado/', views.VistaResultado.as_view(), name='resultado'),
    #ejemplo: /encuesta/2/voto/
    path ('<int:pregunta_id>/voto/', views.voto, name= 'voto'),


]

