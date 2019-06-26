from django.db import models

class Tipo_status(models.Model):
    descripcion = models.CharField(max_length=45)
    class Meta:
        verbose_name = 'Tipo_status'
        verbose_name_plural = 'Tipos_status'
    def __str__(self):
        return self.descripcion
        
    
class Grupo(models.Model):
    nombre = models.CharField(max_length=45)
    cuatrimestre = models.IntegerField()
    ano = models.IntegerField(blank=True, null=True, verbose_name= 'Año*')
    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['nombre']
        
    def __str__(self):
        return '%s, Cuatrimestre: %s' % (self.nombre, self.cuatrimestre)
        
    
class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
        ordering = ['nombre']
    def __str__(self):
        return self.nombre
    
class Tipo_movimiento(models.Model):
    tipo = models.CharField(max_length=45)
    class Meta:
        verbose_name = 'Tipo_movimiento'
        verbose_name_plural = 'Tipos_movimiento'
    def __str__(self):
        return self.tipo
    
class Tipo_calificacion(models.Model):
    descripcion = models.CharField(max_length=45)
    class Meta:
        verbose_name = 'Tipo_calificacion'
        verbose_name_plural = 'Tipos_calificacion'
    def __str__(self):
        return self.descripcion

class Materia(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Materia*')
    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['nombre']
    def __str__(self):
        return self.nombre
    
class Carreras(models.Model):
    nombre = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'
        ordering = ['nombre']
    def __str__(self):
        return self.nombre
    
class Alumno(models.Model):
    nombre = models.CharField(max_length=120, blank=True, null=True)
    matricula = models.CharField(max_length=120,blank=True, null=True)
    generacion_tsu = models.IntegerField(blank=True, null=True)
    generacion_ing = models.IntegerField(blank=True, null=True)
    cuatrimestre = models.IntegerField()
    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    id_carrera = models.ForeignKey(Carreras, on_delete=models.CASCADE, related_name='carrera_tsu', verbose_name='Carrera')
    id_carrera_ing = models.ForeignKey(Carreras, on_delete=models.CASCADE, blank=True, null=True, related_name='carrera_ing')
    id_status_tsu = models.ForeignKey(Tipo_status, on_delete=models.CASCADE, blank=True, null=True, related_name='status_tsu')
    id_status_ing = models.ForeignKey(Tipo_status, on_delete=models.CASCADE, blank=True, null=True, related_name='status_ing')
    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
    def __str__(self):
        return '%s %s' % (self.matricula, self.nombre)

    
class Movimientos(models.Model):
    cuatrimestre = models.IntegerField()
    fecha = models.DateField()
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    id_tipo_movimiento = models.ForeignKey(Tipo_movimiento, on_delete=models.CASCADE)
    id_carrera = models.ForeignKey(Carreras, on_delete=models.CASCADE, verbose_name='Carrera')
    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    #descripcion = models.CharField(max_length=300,blank=True, null=True)
    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
    def __str__(self):
        return '%s del alumn@ %s' % (self.id_tipo_movimiento, self.id_alumno)
        
    def natural_key(self):
        return self.my_natural_key
    
class Horario(models.Model):
    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, verbose_name="Grupos")
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE,verbose_name='Materia')
    id_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, verbose_name="Profesor")
    id_carrera = models.ForeignKey(Carreras, on_delete=models.CASCADE, verbose_name='Carrera')
    cuatrimestre = models.IntegerField(verbose_name="Cuatrimestre")
    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
    def __str__(self):
        return 'Grupo: %s | Materia: %s | Profesor: %s | Carrera: %s | Cuatrimestre: %s' % (self.id_grupo, self.id_materia, self.id_profesor, self.id_carrera, self.cuatrimestre)
    
    
class Calificaciones(models.Model):
    calificacion = models.IntegerField()
    id_horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    id_tipo_calificacion = models.ForeignKey(Tipo_calificacion, on_delete=models.CASCADE, verbose_name='Tipo de Calificación')
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha = models.DateField()
    class Meta:
        verbose_name = 'Calificacion'
        verbose_name_plural = 'Calificaciones'
    def __str__(self):
        return 'Alumno: %s | Calificacion: %s | Tipo: %s | %s'  % (self.id_alumno, self.calificacion, self.id_tipo_calificacion, self.id_horario)