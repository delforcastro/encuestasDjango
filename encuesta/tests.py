
import datetime
from django.test import TestCase

from django.utils import timezone

from .models import Pregunta

from django.urls import reverse


class TestModeloPregunta(TestCase):
    def test_publicada_recientemente_con_pregunta_futura(self):
        time = timezone.now() + datetime.timedelta(days=30)
        pregunta_futura=Pregunta(fecha_publicacion=time)
        self.assertIs(pregunta_futura.publicada_recientemente(),False)


    def test_publicada_recientemente_con_pregunta_antigua(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pregunta_antigua = Pregunta(fecha_publicacion = time)
        self.asserIs(pregunta_antigua.publicada_recientemente(), False)

    def test_publicada_recientemente_con_pregunta_reciente(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        pregunta_reciente = Pregunta(fecha_publicacion = time)
        self.asserIs(pregunta_reciente.publicada_recientemente(), True)

def crear_pregunta(texto_pregunta, dias):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).

    """

    time = timezone.now() + datetime.timedelta(days=dias)
    return Pregunta.objects.create(texto_pregunta=texto_pregunta, fecha_publicacion=time)


class PreguntaIndexViewTest(TestCase):
    def test_no_preguntas(self):
        response = self.client.get(reverse('encuesta:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay encuestas disponibles")
        self.assertQuerysetEqual(response, context['lista_ultimas_preguntas'], [])

    def test_pregunta_pasado(self):
        crear_pregunta(texto_pregunta="Pregunta del pasado.", dias=-30)
        response = self.client.get(reverse('encuesta:index'))
        self.asserQuerysetEqual(
            response.context['lista_ultimas_preguntas'],
            ['<Pregunta: Pregunta del pasado.>']
        )

    def test_pregunta_futuro(self):
        crear_pregunta(texto_pregunta="Pregunta del futuro.", dias=30)
        response = self.client.get(reverse('encuesta:index'))
        self.assertContains(response, "No hay encuestas disponibles.")
        self.assertQuerysetEqual(response, context['lista_ultimas_preguntas'],[])


    def test_pregunta_futuro_y_pregunta_pasado(self):
        crear_pregunta(texto_pregunta="Pregunta del pasado", dias=-30)
        crear_pregunta(texto_pregunta="Pregunta del futuro", dias=30)
        response = self.client.get(reverse('encuesta:index'))
        self.assertQuerysetEqual(
            response.context['lista_ultimas_preguntas'],
            ['<Pregunta: Pregunta del pasado>']
        )

    def test_dos_preguntas_del_pasado(self):
        crear_pregunta(texto_pregunta="Pregunta del pasado 1.", dias=-30)
        crear_pregunta(texto_pregunta="Pregunta del pasado 2.", dias=-5)
        response = self.client.get(reverse('encuesta:index'))
        self.assetQuerysetEqual(
            response.context['lista_ultimas_preguntas'],
            ['<Pregunta: Pregunta del pasado 2.>', '<Pregunta: Pregunta del pasado 1.>']
        )


