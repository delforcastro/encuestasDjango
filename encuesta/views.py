from django.http import HttpResponse, HttpResponseRedirect
#CUIDADO: IMPORTAR EN FORMA ORDENADA ALFABETICAMENTE:
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic



from .models import Pregunta, Respuesta


class VistaIndex(generic.ListView):
    template_name = 'encuesta/index.html'
    context_object_name = 'lista_ultimas_preguntas'

    def get_queryset(self):
        #returna las ultimas 5 preguntas
        return Pregunta.objects.filter(
            fecha_publicacion__lte=timezone.now()
        ).order_by('-fecha_publicacion')[:5]
        #return Pregunta.objects.order_by('fecha_publicacion')[:5]

class VistaDetalle(generic.DetailView):
    model = Pregunta
    template_name = 'encuesta/detalle.html'

    def get_queryset(self):
        return Pregunta.objects.filter(fecha_publicacion__lte=timezone.now())


class VistaResultado (generic.DetailView):
    model = Pregunta
    template_name = 'encuesta/resultado.html'


def voto(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)

    try:
        respuesta_selec = pregunta.respuesta_set.get(pk=request.POST['respuesta'])
    except (KeyError, Respuesta.DoesNotExist):
        #vuelve a mostrar formulario
        return render(request, 'encuesta/detalle.html', {
            'pregunta' : pregunta,
            'error_message' : "No has seleccionado ninguna respuesta.",

        })
    else:
        respuesta_selec.votos += 1
        respuesta_selec.save()

        return HttpResponseRedirect(reverse('encuesta:resultado', args=(pregunta.id,)))

