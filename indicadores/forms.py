from django import forms
from indicadores.models import Alumno, Horario,Calificaciones,Grupo,Materia, Movimientos, Profesor
from django.forms import ModelForm
from betterforms.multiform import MultiModelForm

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = '__all__'

class MovimientosForm(forms.ModelForm):
    class Meta:
        model = Movimientos
        fields = '__all__'
        exclude = ['id_alumno']

class GruposForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = '__all__'

class HorariosForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = '__all__'

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = '__all__'

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = '__all__'

class CalificacionesForm(forms.ModelForm):
    class Meta:
        model = Calificaciones
        fields = '__all__'
        exclude = ['id_alumno', 'id_horario']

class EficienciaterminalForm(forms.ModelForm):
    
    class Meta:
        model = Alumno
        fields = ('id_carrera',)
        
class Resagoform(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ('id_carrera',)
        
class EficienciaDeTitilacionForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ('id_carrera',)
    
#class Retencionform(forms.ModelForm):
    
    
class AbandonoEscolar(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ('id_carrera',)
    
class tipocaliform(forms.ModelForm):
    class Meta:
        model = Calificaciones
        fields = ('id_tipo_calificacion',)
        
class Reprobacionform(forms.ModelForm):
    
    class Meta:
        model = Horario
        fields = ('id_grupo',)

class reprobacionmaterH(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ('id_carrera','id_materia')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_materia'].queryset = Materia.objects.none()

class reprobaciongrupoH(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ('id_carrera','id_grupo')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_grupo'].queryset = Grupo.objects.none()
        

class reprobacionmaterM(forms.ModelForm):
    class Meta:
        model = Grupo
        fields =('ano','cuatrimestre')
    def __init__(self, *args, **kwargs):
        super(reprobacionmaterM,self).__init__(*args, **kwargs)
        self.fields['ano'].value='2019'
        self.fields['cuatrimestre'].max=11
        self.fields['cuatrimestre'].min=1

        
#-------------------------------------------------------------------------------------------------#        
class rmhm(MultiModelForm):
    form_classes={
        'Reph':reprobacionmaterM,
        'Repm':reprobacionmaterH,
    }
    
class rghm(MultiModelForm):
    form_classes={
        'Reph':reprobacionmaterM,
        'Repm':reprobaciongrupoH,
    }
    