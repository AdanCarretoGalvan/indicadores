from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from indicadores.views import index,reprobaciongen,reprobacionMateria,desersion,logout_request,reprobacioncar ,home, eficienciaTerminal, eficienciaDeTitulacion, indiceDeReprobacion, resago, abandonoEscolar, retencion
from .validaciones import valida, alumnos, alumAjax, movimientos_list, MovimientosUpdate, \
AlumnoUpdate, carreras_list, grupos_list, gruposAjax, GruposUpdate, horarios_list, HorariosUpdate, horariosAjax, \
calificaciones, calificacionAjax, CalificacionUpdate, materias_list, MateriaUpdate, profesores_list, ProfesorUpdate, movAjax
from .importaciones import importa

urlpatterns = [
    url(r'^eficienciaterminal/$', login_required(eficienciaTerminal), name='eftter'),
    url(r'^eficienciadetitulacion/$', login_required(eficienciaDeTitulacion), name='eftit'),
    url(r'^indicedereprobacion/$', login_required(indiceDeReprobacion), name='inderep'),
    url(r'^resago/$', login_required(resago),name='resago'),
    url(r'^reprobacioncar/$', login_required(reprobacioncar),name='reprobacioncar'),
    url(r'^reprobacionmateria/$', login_required(reprobacionMateria),name='reprobacionmateria'),
    url(r'^abandonoescolar/$', login_required(abandonoEscolar), name='abes'),
    url(r'^retencion/$', login_required(retencion), name='retencion'),
    url(r'^$', login_required(home), name='menu'),
    url(r'^accounts/logout/$', login_required(logout_request), name='milogout'),
    url(r'^accounts/login/$', index , name='index'),
    url(r'^reprobaciongen/$', login_required(reprobaciongen),name='reprobaciongen'),
    url(r'^desersion/$', login_required(desersion),name='desersion'),
    path('llenamateria/', views.llenamateria, name='llenamateria'),
    path('llenagrupo/', views.llenagrupo, name='llenagrupo'),
    #URLS PARA VALIDACION DE DATOS#
    url(r'^validar/$', login_required(valida), name='valida'),
    url(r'^lista_al/$', login_required(alumnos), name='alumno_list'),
    url(r'^alumajax/$', login_required(alumAjax), name='alumajax'),
    url(r'^editar_alum/(?P<pk>.+)/$', login_required(AlumnoUpdate.as_view()), name='editar_alum'),
    url(r'^lista_mov/$', login_required(movimientos_list), name='mov_list'),
    url(r'^movajax/$', login_required(movAjax), name='movajax'),
    url(r'^editar_mov/(?P<pk>.+)/$',login_required(MovimientosUpdate.as_view()), name="editar_mov"),
    url(r'^lista_car/$', login_required(carreras_list), name="carreras_list"),
    url(r'^lista_grupo/$', login_required(grupos_list), name="grupos_list"),
    url(r'^gruposajax/$', login_required(gruposAjax), name='gruajax'),
    url(r'^editar_grupo/(?P<pk>.+)/$',login_required(GruposUpdate.as_view()), name="editar_grupo"),
    url(r'^lista_horario/$', login_required(horarios_list), name="horarios_list"),
    url(r'^horariosajax/$', login_required(horariosAjax), name='horajax'),
    url(r'^editar_horario/(?P<pk>.+)/$',login_required(HorariosUpdate.as_view()), name="editar_horario"),
    url(r'^lista_cal/$', login_required(calificaciones), name='cali_list'),
    url(r'^calificacionajax/$', login_required(calificacionAjax), name='caliajax'),
    url(r'^editar_cali/(?P<pk>.+)/$', login_required(CalificacionUpdate.as_view()), name='editar_cali'),
    url(r'^lista_mat/$', login_required(materias_list), name='lista_mat'),
    url(r'^editar_mat/(?P<pk>.+)/$', login_required(MateriaUpdate.as_view()), name='editar_mat'),
    url(r'^lista_profe/$', login_required(profesores_list), name='profe_list'),
    url(r'^editar_profe/(?P<pk>.+)/$', login_required(ProfesorUpdate.as_view()), name='editar_profe'),
    #URLS PARA IMPORTAR DATOS#
    url(r'^importar/$', login_required(importa), name='importa'),

]