from django.contrib import admin
from indicadores.models import Tipo_status, Grupo, Profesor, Tipo_movimiento, Tipo_calificacion, Materia, Carreras, Alumno,  Movimientos, Horario, Calificaciones
from import_export.admin import ImportExportModelAdmin


@admin.register(Tipo_status, Grupo, Profesor, Tipo_movimiento, Tipo_calificacion, Materia, Carreras)
class ViewAdmin(ImportExportModelAdmin):
    pass

class AlumnoAdmin(ImportExportModelAdmin):
    list_display=('nombre','matricula','cuatrimestre',)
    search_fields=('nombre','matricula',)
    list_filter=('cuatrimestre','id_carrera','generacion_tsu','id_carrera_ing','generacion_ing',)
    
class MovimientosAdmin(ImportExportModelAdmin):
    list_display=('id_tipo_movimiento','cuatrimestre','fecha','id_alumno',)
    search_fields=('id_alumno','id_tipo_movimiento',)
    list_filter=('cuatrimestre',)
    
class HorarioAdmin(ImportExportModelAdmin):
    list_display=('id_grupo','id_materia','id_profesor','id_carrera','cuatrimestre',)
    search_fields=('id_grupo','id_materia','id_profesor','id_carrera',)
    list_filter=('cuatrimestre','id_carrera',)

class CalificacionesAdmin(ImportExportModelAdmin):
    list_display=('id_alumno','calificacion','id_tipo_calificacion','fecha',)
    search_fields=('id_alumno',)
    list_filter=('id_tipo_calificacion','calificacion',)
    
#class Tipo_statusAdmin(ImportExportModelAdmin):
 #   search_fields=('id_alumno',)
    
#class GrupoAdmin(ImportExportModelAdmin):
#    search_fields=('id_alumno',)
    
#class ProfesorAdmin(ImportExportModelAdmin):
#    search_fields=('id_alumno',)
    
#class Tipo_movimientoAdmin(ImportExportModelAdmin):
#    search_fields=('id_alumno',)

#class Tipo_calificacionAdmin(ImportExportModelAdmin):
#   search_fields=('id_alumno',)

#class MateriaAdmin(ImportExportModelAdmin):
#    search_fields=('id_alumno',)

#class CarrerasAdmin(ImportExportModelAdmin):
 #   search_fields=('id_alumno',)
    
#admin.site.register(Tipo_status)
#admin.site.register(Grupo)
#admin.site.register(Profesor)
#admin.site.register(Tipo_movimiento)
#admin.site.register(Tipo_calificacion)
#admin.site.register(Materia)
#admin.site.register(Carreras)
admin.site.register(Alumno,AlumnoAdmin)
admin.site.register(Movimientos,MovimientosAdmin)
admin.site.register(Horario,HorarioAdmin)
admin.site.register(Calificaciones,CalificacionesAdmin)