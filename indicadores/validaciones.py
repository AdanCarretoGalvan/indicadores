from django.shortcuts import render
from indicadores.models import Tipo_movimiento, Alumno, Movimientos, Calificaciones, Tipo_status, Grupo, Carreras, Horario, Materia, Profesor
from django.views.generic import ListView, UpdateView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from .forms import MovimientosForm, AlumnoForm, GruposForm, HorariosForm, CalificacionesForm, MateriaForm, ProfesorForm
from django.core import serializers

def valida(request):
    return render(request, "validaciones/validar_datos.html")

def alumnos(request):
	return render(request, "validaciones/alumnos_list.html")

def alumAjax(request):
	cuatri = request.GET.get('cuatri')
	alumno = Alumno.objects.filter(cuatrimestre = cuatri)
	json = serializers.serialize('json', alumno)
	return HttpResponse(json, content_type='application/json')

class AlumnoUpdate(UpdateView):
	model = Alumno
	form_class = AlumnoForm
	template_name = 'formularios/alum_form.html'
	success_url = reverse_lazy('alumno_list')

def movimientos_list(request):
	 return render(request, "validaciones/movimientos_list.html")

def movAjax(request):
	id_mov = request.GET.get('id')
	lista = Movimientos.objects.filter(id__gte = id_mov)
	json = serializers.serialize('json', lista)
	return HttpResponse(json, content_type='application/json')

class MovimientosUpdate(UpdateView):
	model = Movimientos
	form_class = MovimientosForm
	template_name = 'formularios/mov_form.html'
	success_url = reverse_lazy('mov_list')

def carreras_list(request):
	carrera = Carreras.objects.all()
	return render(request, "validaciones/carreras_list.html", {'carreras': carrera})

def grupos_list(request):
	return render(request, "validaciones/grupos_list.html")

def gruposAjax(request):
	cuatrimestre = request.GET.get('cuatri')
	anio = request.GET.get("anio")
	grupo = Grupo.objects.filter(cuatrimestre=cuatrimestre, ano=anio)
	json = serializers.serialize('json', grupo)
	return HttpResponse(json, content_type='application/json')

class GruposUpdate(UpdateView):
	model = Grupo
	form_class = GruposForm
	template_name = 'formularios/grupos_form.html'
	success_url = reverse_lazy('grupos_list')

def horarios_list(request):
	return render(request, "validaciones/horarios_list.html")

def horariosAjax(request):
	cuatrimestre = request.GET.get('cuatri')
	horario = Horario.objects.filter(cuatrimestre=cuatrimestre)
	json = serializers.serialize('json', horario)
	return HttpResponse(json, content_type='application/json')

class HorariosUpdate(UpdateView):
	model = Horario
	form_class = HorariosForm
	template_name = 'formularios/horario_form.html'
	success_url = reverse_lazy('horarios_list')

def calificaciones(request):
	return render(request, "validaciones/cali_list.html")

def calificacionAjax(request):
    id_cal = request.GET.get('id')
    calificacion = Calificaciones.objects.filter(id__gte = id_cal)
    json = serializers.serialize('json', calificacion)
    return HttpResponse(json, content_type='application/json')

class CalificacionUpdate(UpdateView):
	model = Calificaciones
	form_class = CalificacionesForm
	template_name = 'formularios/cali_form.html'
	success_url = reverse_lazy('cali_list')

def materias_list(request):
	materia = Materia.objects.all()
	return render(request, "validaciones/materias_list.html", {'materias':materia})

class MateriaUpdate(UpdateView):
	model = Materia
	form_class = MateriaForm
	template_name = 'formularios/materia_form.html'
	success_url = reverse_lazy('lista_mat')

def profesores_list(request):
	profe = Profesor.objects.all()
	return render(request, "validaciones/profesor_list.html", {'profe':profe})

class ProfesorUpdate(UpdateView):
	model = Profesor
	form_class = ProfesorForm
	template_name = 'formularios/profe_form.html'
	success_url = reverse_lazy('profe_list')