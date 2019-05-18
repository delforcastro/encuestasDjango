import datetime
from django.db import models
from django.utils import timezone

class Pregunta(models.Model):
    texto_pregunta = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField('fecha publicada')

    def __str__(self):
        return self.texto_pregunta

    def publicada_recientemente(self):
        ahora = timezone.now()
        return ahora - datetime.timedelta(days=1) <= self.fecha_publicacion <= ahora



class Respuesta(models.Model):
    respuesta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto_respuesta = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.texto_respuesta

