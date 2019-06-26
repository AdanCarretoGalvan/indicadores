from django.shortcuts import render
from indicadores.models import Tipo_movimiento, Alumno, Movimientos, Calificaciones, Tipo_status, Grupo, Carreras, Horario, Materia, Profesor
from django.views.generic import ListView, UpdateView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from .forms import MovimientosForm, AlumnoForm, GruposForm, HorariosForm, CalificacionesForm, MateriaForm, ProfesorForm

def importa(request):
    return render(request, "importar/importarDatos.html")