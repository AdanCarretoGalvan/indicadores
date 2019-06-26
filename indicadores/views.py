from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from indicadores.models import Tipo_status, Grupo, Profesor, Tipo_movimiento, Tipo_calificacion, Materia, Carreras, Alumno,  Movimientos, Horario, Calificaciones
from django.contrib.auth.models import User
from indicadores.forms import EficienciaterminalForm, rmhm,rghm,reprobacionmaterH, reprobaciongrupoH, reprobacionmaterM,Resagoform, EficienciaDeTitilacionForm, AbandonoEscolar,Reprobacionform,tipocaliform
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from random import randint
import datetime
import json
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView

def home(request):
    return render(request, "index/menu.html")

def llenagrupo(request):
    carrera=request.GET.get('carrera')
    yr=request.GET.get('yea')
    cua=request.GET.get('cua')
    geu=Grupo.objects.filter(cuatrimestre = cua , ano=yr).values_list('id',flat = True).distinct()
    grupos=Horario.objects.filter(id_carrera=carrera ).values_list('id_grupo',flat = True).distinct()
    comparacion = [item for item in geu if item in grupos]
    dat=Grupo.objects.filter(id__in=comparacion)
    return render(request,"indica/llenagrupo.html",{'grupos':dat})
    
def llenamateria(request):
    carrera=request.GET.get('carrera')
    yr=request.GET.get('yea')
    cua=request.GET.get('cua')
    geu=Grupo.objects.filter(cuatrimestre = cua , ano=yr).values_list('id',flat = True).distinct()
    grupos=Horario.objects.filter(id_carrera=carrera ).values_list('id_grupo',flat = True).distinct()
    comparacion = [item for item in geu if item in grupos]
    mat=Horario.objects.filter(id_grupo__in=comparacion ).values_list('id_materia',flat = True).distinct()
    materias=Materia.objects.filter(id__in=mat)
    return render(request,"indica/llenamateria.html",{'materias':materias})
    
def reprobacionMateria(request):
    #llama los formularios a mostrar en la plantilla html
    form = reprobacionmaterM()
    form1= reprobacionmaterH()
    form2 = tipocaliform()
    bandera = 0
    #revisar si el metodo de envio de datos es post para que haga el proceso definido dentro de el bloque de codigo
    if request.method == 'POST':
        #Tomar los valores que fueron enviados atraves del formulrio para asignarlos a variables 
        tipocal = request.POST['id_tipo_calificacion']
        carrera=request.POST['id_carrera']
        yr=request.POST['ano']
        materia=request.POST['id_materia']
        cua=request.POST['cuatrimestre']
        tipo = request.POST['tipo']
        #Declarar variables y listas que usaremos en la busqueda de informacion
        nommat=Materia.objects.get(id=materia)
        care = Carreras.objects.get(id=carrera)
        anio=int(yr)
        cat=int(cua)
        bandera = 1
        mater=[]
        series=[]
        nomg=[]
        lsi=[]
        total=0
        noma=[]
        #hacer consultas para sacar los grupos y que apartir de esto se saque su reprobacion
        geu=Grupo.objects.filter(cuatrimestre = cat , ano=anio).values_list('id',flat = True).distinct()
        grupos=Horario.objects.filter(id_carrera=carrera ).values_list('id_grupo',flat = True).distinct()
        comparacion = [item for item in geu if item in grupos]

        #ciclo for para sacar la reprobacion de cada grupo
        for a in comparacion:
            #declarar variables y metodos que usaremos mas adelante
            reproba=[]
            grup= Grupo.objects.get(id=a)
            gru=str(grup.nombre)
            repma=0
            #sacar los profesores de la materia por cada grupo
            profe=Horario.objects.filter(id_grupo=a,id_materia=materia,id__in=(Calificaciones.objects.filter(id_tipo_calificacion=tipocal).values_list("id_horario",flat=True).distinct()))
            for pro in profe:
                profesor=str(pro.id_profesor)
            #Sacar los horarios que se usan y a partir de ellos obtener sus alumnos reprobados
            horarios = Horario.objects.filter(id_grupo=a,id_materia=materia).values_list('id',flat = True).distinct()
            for l in horarios:
                repro= Calificaciones.objects.filter(id_tipo_calificacion=tipocal , calificacion__lt=8 , id_horario=l)
                repma=repma+len(repro)
            #agregar los alumnos repobados a una lista para poder ser mostrados en la grafica
            reproba.append(repma)
            #Enviar datos a la grafica para mostrarla
            total=total+repma
            lsi.append({'grupo':gru,'rep':repma,'profe':profesor})
            data = {
                'name': gru,
                'data': reproba,
            }
            series.append(data)
                
        chart = {
            'chart': {'type':tipo},
            'xAxis': {'categories': ' '},
            'title': {'text': 'Índice de reprobación - Asignatura/Profesor'},
            'subtitle': {'text': str(care) + " / ( " + str(nommat.nombre) +" ) "},
            'plotOptions': {
                    'series': {
                        'borderWidth': 0,
                        'dataLabels': {
                            'enabled': True,
                            'format': '{point.y:.1f}'
                        }
                    }
            },
            'tooltip': {
                'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> of total<br/>'
            },
            'series': series
        }
    
        dump = json.dumps(chart)
        #Reenviar lo obtenido al formulario para poder mostrar la grafica
        return render(request,"indica/reprobacionmateria.html",{'form':form,'lsi':lsi,'total':total,'form2':form2,'form1':form1,'chart':dump,'bandera': bandera})
    #Reenviar los formularios para hacer uso de ellos en la busqueda de datos
    return render(request,"indica/reprobacionmateria.html",{'form':form, 'form1':form1,'form2':form2,'bandera': bandera})


def reprobaciongen(request):
    form = EficienciaterminalForm()
    form1= tipocaliform()
    if request.method == 'POST':
        tipo = request.POST['tipo']
        tipocal = request.POST['id_tipo_calificacion']
        carrera=request.POST['id_carrera']
        yr=request.POST['yr']
        cua=request.POST['cua']
        anio=int(yr)
        cat=int(cua)
        care = Carreras.objects.get(id=carrera)
        bandera = 1
        reproba=[]
        nomg=[]
        geu=Grupo.objects.filter(cuatrimestre = cat , ano=anio).values_list('id',flat = True).distinct()
        grupos=Horario.objects.filter(id_carrera=carrera ).values_list('id_grupo',flat = True).distinct()
        comparacion = [item for item in geu if item in grupos]
        for a in comparacion:
            reo=0
            grup= Grupo.objects.get(id=a)
            gru=str(grup.nombre)
            nomg.append(gru)
            horarios = Horario.objects.filter(id_grupo=a)
            for asd in horarios:
                repro= Calificaciones.objects.filter(id_tipo_calificacion=tipocal , calificacion__lt=8 , id_horario=asd.id)
                reo=reo+len(repro)
            reproba.append(reo)
        data = {
                'name': 'Reprobacion',
                'data': reproba,
            }
        chart = {
            'chart': {'type': tipo},
            'xAxis': {'categories': nomg},
            'title': {'text': 'Indice de reprobacion'},
            'subtitle':{'text': str(care)},
            'plotOptions': {
                    'series': {
                        'borderWidth': 0,
                        'dataLabels': {
                            'enabled': True,
                            'format': '{point.y:.1f}'
                        }
                    }
            },
            'tooltip': {
                'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> of total<br/>'
            },
            'series': [data]
        }

        dump = json.dumps(chart) 
        return render(request,"indica/reprobacionmateria.html",{'form':form,'form1':form1,'chart':dump})
    return render(request,"indica/reprobacionmateria.html",{'form':form,'form1':form1})

def reprobacioncar(request):
    form = EficienciaterminalForm()
    form1= tipocaliform()
    bandera = 0
    if request.method == 'POST':
        tipocal = request.POST['id_tipo_calificacion']
        carrera=request.POST['id_carrera']
        yr=request.POST['year']
        cua=request.POST['cuatrimestre']
        tipo = request.POST['tipo']
        bandera = 1
        anio=int(yr)
        cat=int(cua)
        care = Carreras.objects.get(id=carrera)
        mater=[]
        series=[]
        nomg=[]
        noma=[]
        geu=Grupo.objects.filter(cuatrimestre = cat , ano=anio).values_list('id',flat = True).distinct()
        grupos=Horario.objects.filter(id_carrera=carrera ).values_list('id_grupo',flat = True).distinct()
        comparacion = [item for item in geu if item in grupos]
        for a in comparacion:
            grup= Grupo.objects.get(id=a)
            gru=str(grup.nombre)
            nomg.append(gru)
            mat=Horario.objects.filter(id_grupo=a ).values_list('id_materia',flat = True).distinct()
            for si in mat:
                if si not in mater:
                    mater.append(si)
        for a in mater:
            nomma=Materia.objects.get(id=a)
            noma.append(str(nomma.nombre))
            
        for a in comparacion:
            reproba=[]
            grup= Grupo.objects.get(id=a)
            gru=str(grup.nombre)
            for i in mater:
                repma=0
                horarios = Horario.objects.filter(id_grupo=a,id_materia=i).values_list('id',flat = True).distinct()
                for l in horarios:
                    repro= Calificaciones.objects.filter(id_tipo_calificacion=tipocal , calificacion__lt=8 , id_horario=l)
                    repma=repma+len(repro)
                reproba.append(repma)
            data = {
                'name': gru,
                'data': reproba,
            }
            series.append(data)
                
        chart = {
            'chart': {'type': tipo},
            'xAxis': {'categories': noma},
            'title': {'text': 'Índice de reprobación - Grupo/Asignatura'},
            'subtitle':{'text': str(care)},
            'plotOptions': {
                    'series': {
                        'borderWidth': 0,
                        'dataLabels': {
                            'enabled': True,
                            'format': '{point.y:.1f}'
                        }
                    }
            },
            'tooltip': {
                'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> of total<br/>'
            },
            'series': series
        }
    
        dump = json.dumps(chart)
        return render(request,"indica/reprobacioncar.html",{'form':form,'form1':form1,'chart':dump, 'bandera':bandera})
    else:
        bandera = 0
    return render(request,"indica/reprobacioncar.html",{'form':form,'form1':form1, 'bandera':bandera})

def reprobaciongen(request):
    #LLAmar formularios para enviar los datos
    form = EficienciaterminalForm()
    form1= tipocaliform()
    bandera = 0
    #revisar si lo que se evia es el metodo post
    if request.method == 'POST':
        #Obtener datos enviados a traves del formulario
        tipo = request.POST['tipo']
        tipocal = request.POST['id_tipo_calificacion']
        carrera=request.POST['id_carrera']
        yr=request.POST['year']
        cua=request.POST['cuatrimestre']
        #Crear variables,listas, etc para usar mas adelante
        anio=int(yr)
        cat=int(cua)
        care = Carreras.objects.get(id=carrera)
        bandera = 1
        reproba=[]
        total=0
        nomg=[]
        #obtener los grupos que nesesitaremos en la busqueda
        geu=Grupo.objects.filter(cuatrimestre = cat , ano=anio).values_list('id',flat = True).distinct()
        grupos=Horario.objects.filter(id_carrera=carrera ).values_list('id_grupo',flat = True).distinct()
        comparacion = [item for item in geu if item in grupos]
        #sacar la cantidad de reprobados por cada grupo
        for a in comparacion:
            reo=0
            grup= Grupo.objects.get(id=a)
            gru=str(grup.nombre)
            nomg.append(gru)
            horarios = Horario.objects.filter(id_grupo=a)
            for asd in horarios:
                repro= Calificaciones.objects.filter(id_tipo_calificacion=tipocal , calificacion__lt=8 , id_horario=asd.id)
                reo=reo+len(repro)
            #agragar los datos a una lista
            reproba.append(reo)
        #Enviar datos a la grafica para mostrarla
        tam=len(reproba)
        lsi=[]
        for a in range(0,tam):
            lsi.append({'grupo':nomg[a],'rep':reproba[a]})
        data = {
                'name': 'Grupo',
                'data': reproba,
            }
        chart = {
            'chart': {'type': tipo},
            'xAxis': {'categories': nomg},
            'title': {'text': 'Índice de reprobación por grupo'},
            'subtitle':{'text': str(care)},
            'plotOptions': {
                    'series': {
                        'borderWidth': 0,
                        'dataLabels': {
                            'enabled': True,
                            'format': '{point.y:.2f}'
                        }
                    }
            },
            'tooltip': {
                #'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                #'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> of total<br/>'
            },
            'series': [data]
        }
        
            
        for a in reproba:    
            total=total+a        
        dump = json.dumps(chart)
        #Reenviar lo obtenido al formulario para poder mostrar la grafica
        return render(request,"indica/reprobaciongeneral.html",{'form':form,'lsi':lsi,'reproba':reproba,'total':total,'form1':form1,'chart':dump, 'bandera':bandera})
    #Reenviar los formularios para hacer uso de ellos en la busqueda de datos
    else:
        bandera = 0
    return render(request,"indica/reprobaciongeneral.html",{'form':form,'form1':form1, 'bandera':bandera})

def logout_request(request):
    logout(request)
    #messages.info(request,"Secion cerrada correctamente")
    return redirect("index")

def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #messages.info(request, f"Accediste con el usuario {username}")
                return redirect('/')
            else:
                messages.error(request, "Usuario y/o cotraseña erroneos")
        else:
            messages.error(request, "Usuario y/o cotraseña erroneos")
    form = AuthenticationForm()
    return render(request = request, template_name = "login.html")

def eficienciaTerminal(request):
    form = EficienciaterminalForm()
    hoy = datetime.date.today()
    yea = hoy.year
    bandera = 0;
    if request.method == 'POST':
        carrera = request.POST['id_carrera']
        inicio =  request.POST['ain']
        fin = request.POST['afi']
        tipo = request.POST['tipo']
        inran=int(inicio)
        firan=int(fin)
        care = Carreras.objects.get(id=carrera)
        bandera = 1
        datos=[]
        pie=[]
        colors=[]
        care= Carreras.objects.get(id=carrera)
        let=str(care.nombre)[:3].lower()
        if inran>firan:
            rango = list(range(firan,inran+1))
        else:
            rango = list(range(inran,firan+1))
            
        for col in rango:
            pie.append("Sep "+str(col)+' - Ago '+str(col+2))
            
        if let=='ing':
            for generacion in rango:
                cortetsu = Movimientos.objects.filter(Q(id_tipo_movimiento=1)|Q(id_tipo_movimiento=2),cuatrimestre=7,id_carrera=int(carrera),fecha__year=generacion).values_list('id_alumno',flat = True).distinct()
                alumTittsu = Movimientos.objects.filter(id_carrera=int(carrera), id_tipo_movimiento = (Tipo_movimiento.objects.get(tipo='Titulacion' ))).values_list('id_alumno',flat = True).distinct()
                comparacion = [item for item in alumTittsu if item in cortetsu]
                corte=len(cortetsu)
                titulados=len(comparacion)
                try: 
                    efi= (titulados/corte)*100
                except ZeroDivisionError:
                    efi=0
                datos.append(efi)
                pie.append("Sep "+str(generacion)+" - Ago "+str(generacion+2))
        else:
            for generacion in rango:
                cortetsu = Movimientos.objects.filter(id_tipo_movimiento=1,cuatrimestre=1,id_carrera=int(carrera),fecha__year=generacion).values_list('id_alumno',flat = True).distinct()
                alumTittsu = Movimientos.objects.filter(id_carrera=int(carrera), id_tipo_movimiento = (Tipo_movimiento.objects.get(tipo='Titulacion' ))).values_list('id_alumno',flat = True).distinct()
                comparacion = [item for item in alumTittsu if item in cortetsu]
                corte=len(cortetsu)
                titulados=len(comparacion)
                try: 
                    efi= (titulados/corte)*100
                except ZeroDivisionError:
                    efi=0
                datos.append(efi)
                pie.append("Sep "+str(generacion)+" - Ago "+str(generacion+2))
        data = {
            'name': 'Generaciones',
            'data': datos,
        }
        chart = {
            'chart': {'type': tipo},
            'xAxis': {'categories': pie},
            'title': {'text': 'Índice de eficiencia terminal'},
            'subtitle': {'text':str(care)},
            'plotOptions': {
                    'series': {
                        'borderWidth': 0,
                        'dataLabels': {
                            'enabled': True,
                            'format': '{point.y:.1f}' + ' %'
                        }
                    }
            },
            'tooltip': {
                'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> %  of total<br/>'
            },
            'series': [data]
        }
        dump = json.dumps(chart)
        return render(request, 'indica/eficiencia_terminal.html', {'chart': dump,'yea':yea,'care':care,'form': form,'datos':datos, 'tipo':tipo,'fin' : fin, 'inicio' : inicio,'rango':rango,'bandera': bandera})
    else:
        bandera = 0
    return render(request, 'indica/eficiencia_terminal.html', {'yea':yea,'form': form, 'bandera': bandera})

def eficienciaDeTitulacion(request):
    form = EficienciaDeTitilacionForm()
    hoy = datetime.date.today()
    yea = hoy.year
    if request.method == 'POST':
        carrera = request.POST['id_carrera']
        inicio =  request.POST['ain']
        fin = request.POST['afi']
        tipo = request.POST['tipo']
        inran=int(inicio)
        firan=int(fin)
        care = Carreras.objects.get(id=carrera)
        datos=[]
        pie=[]
        colors=['blue']
        care= Carreras.objects.get(id=carrera)
        let=str(care.nombre)[:3].lower()
        if inran>firan:
            rango = list(range(firan,inran+1))
        else:
            rango = list(range(inran,firan+1))
                
            
        if let=='ing':
            for generacion in rango:
                cortetsu = Movimientos.objects.filter(Q(id_tipo_movimiento=1)|Q(id_tipo_movimiento=2),cuatrimestre=7,id_carrera=int(carrera),fecha__year=generacion).values_list('id_alumno',flat = True).distinct()
                alumTittsu = Movimientos.objects.filter(id_carrera=int(carrera), id_tipo_movimiento = (Tipo_movimiento.objects.get(tipo='Titulacion' ))).values_list('id_alumno',flat = True).distinct()
                alumegtsu = Movimientos.objects.filter(id_carrera=int(carrera), id_tipo_movimiento = (Tipo_movimiento.objects.get(tipo='Egreso' ))).values_list('id_alumno',flat = True).distinct()
                comparacion = [item for item in alumTittsu if item in cortetsu]
                comparacion2 = [item for item in alumegtsu if item in cortetsu]
                egresados=len(comparacion2)
                titulados=len(comparacion)
                try: 
                    efi= (titulados/egresados)*100
                except ZeroDivisionError:
                    efi=0
                datos.append(efi)
                pie.append("Sep "+str(generacion)+" - Ago "+str(generacion+2))
        else:
            for generacion in rango:
                cortetsu = Movimientos.objects.filter(id_tipo_movimiento=1,cuatrimestre=1,id_carrera=int(carrera),fecha__year=generacion).values_list('id_alumno',flat = True).distinct()
                alumTittsu = Movimientos.objects.filter(id_carrera=int(carrera), id_tipo_movimiento = (Tipo_movimiento.objects.get(tipo='Titulacion' ))).values_list('id_alumno',flat = True).distinct()
                alumegtsu = Movimientos.objects.filter(id_carrera=int(carrera), id_tipo_movimiento = (Tipo_movimiento.objects.get(tipo='Egreso' ))).values_list('id_alumno',flat = True).distinct()
                comparacion = [item for item in alumTittsu if item in cortetsu]
                comparacion2 = [item for item in alumegtsu if item in cortetsu]
                egresados=len(comparacion2)
                titulados=len(comparacion)
                try: 
                    efi= (titulados/egresados)*100
                except ZeroDivisionError:
                    efi=0
                datos.append(efi)
                pie.append("Sep "+str(generacion)+" - Ago "+str(generacion+2))
        data = {
            'name': 'Generaciones',
            'data': datos,
        }
        chart = {
            'chart': {'type': tipo},
            'xAxis': {'categories': pie},
            'title': {'text': 'Índice de eficiencia de titulación'},
            'subtitle': {'text':str(care)},
            'plotOptions': {
                    'series': {
                        'borderWidth': 0,
                        'dataLabels': {
                            'enabled': True,
                            'format': '{point.y:.1f}' +' %'
                        }
                    }
            },
            'tooltip': {
                'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> %  of total<br/>'
            },
            'series': [data]
        }

        dump = json.dumps(chart)        
        return render(request, 'indica/eficiencia_de_titulacion.html', {'chart': dump,'yea': yea ,'care':care,'form': form,'datos':datos, 'tipo':tipo,'fin' : fin, 'inicio' : inicio,'rango':rango})
    else: 
        bandera = 0
    return render(request, 'indica/eficiencia_de_titulacion.html', {'form': form,'yea':yea})

def indiceDeReprobacion(request):
    form = reprobacionmaterM()
    form1= reprobaciongrupoH()
    form2 = tipocaliform()
    numrep=[]
    mater=[]
    bandera = 0
    if request.method == 'POST':
        carrera = request.POST['id_carrera']
        grupo = request.POST['id_grupo']
        tipocal = request.POST['id_tipo_calificacion']
        tipo = request.POST['tipo']
        series=[]
        bandera = 1
        horarios = Horario.objects.filter(id_grupo=grupo)
        grup= Grupo.objects.get(id=grupo)
        gru=str(grup.nombre)
        care = Carreras.objects.get(id=carrera)
        for a in horarios:
            repro= Calificaciones.objects.filter(id_tipo_calificacion=tipocal , calificacion__lt=8 , id_horario=a.id).count()
            numrep.append(repro)
            mater.append('Materia: '+ str(a.id_materia) + ', Profesor: '+str(a.id_profesor))
            
        data = {
            'name': gru,
            'data': numrep,
        }
        series.append(data)
        chart = {
            'chart': {'type': tipo},
            'xAxis': {'categories': mater},
            'title': {'text': 'Índice de reprobación - Grupo/Asignatura/Profesor'},
            'subtitle':{'text': str(care)},
            'plotOptions': {
                    'series': {
                        'borderWidth': 0,
                        'dataLabels': {
                            'enabled': True,
                            'format': '{point.y:.1f}'
                        }
                    }
            },
            'tooltip': {
                'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> of total<br/>'
            },
            'series': series
        }

        dump = json.dumps(chart) 
        return render(request, 'indica/indice_de_reprobacion.html', {'chart': dump,'numrep':numrep,'horarios':horarios,'form': form,'form1': form1,'form2':form2, 'bandera': bandera})
    else:
        bandera = 0
    return render(request, 'indica/indice_de_reprobacion.html', {'form': form,'form1': form1,'form2':form2, 'bandera': bandera})

def resago(request):
    hoy = datetime.date.today()
    yea = hoy.year
    form = Resagoform()
    bandera = 0
    if request.method == 'POST':
        carrera = request.POST['id_carrera']
        inicio =  request.POST['ain']
        fin = request.POST['afi']
        tipo = request.POST['tipo']
        inran=int(inicio)
        firan=int(fin)
        
        bandera = 1
        datos=[]
        pie=[]
        care= Carreras.objects.get(id=carrera)
        let=str(care.nombre)[:3].lower()
        if inran>firan:
            rango = list(range(firan,inran+1))
        else:
            rango = list(range(inran,firan+1))
        Alrei = Movimientos.objects.filter(id_carrera=carrera,id_tipo_movimiento=(Tipo_movimiento.objects.get(tipo='Reingreso'))).values_list('id_alumno',flat = True).distinct()
        if let=='ing':
            for generacion in rango:
                cortetsu = Alumno.objects.filter( Q(id_status_ing = (Tipo_status.objects.get(descripcion='Activo' ))) | Q(id_status_ing = (Tipo_status.objects.get(descripcion='Egresado' ))) | Q(id_status_ing = (Tipo_status.objects.get(descripcion='Titulado' ))),id_carrera_ing=int(carrera),generacion_ing=generacion)
                lista=[]
                for a in cortetsu:
                    lista.append(a.id)
                comparacion = [item for item in Alrei if item in lista]
                tam=len(comparacion)
                datos.append(tam)
                pie.append("Sep "+str(generacion)+" - Ago "+str(generacion+2))
                
        else:
            for generacion in rango:
                cortetsu = Alumno.objects.filter( Q(id_status_tsu = (Tipo_status.objects.get(descripcion='Activo' ))) | Q(id_status_tsu = (Tipo_status.objects.get(descripcion='Egresado' ))) | Q(id_status_tsu = (Tipo_status.objects.get(descripcion='Titulado' ))),id_carrera=int(carrera),generacion_tsu=generacion)
                lista=[]
                for a in cortetsu:
                    lista.append(a.id)
                comparacion = [item for item in Alrei if item in lista]
                tam=len(comparacion)
                datos.append(tam)
                pie.append("Sep "+str(generacion)+" - Ago "+str(generacion+2))
        data = {
            'name': 'Generaciones',
            'data': datos,
        }
        chart = {
            'chart': {'type': tipo},
            'xAxis': {'categories': pie},
            'title': {'text': 'Índice de rezago'},
            'subtitle':{'text': str(care)},
            'plotOptions': {
                    'series': {
                        'borderWidth': 0,
                        'dataLabels': {
                            'enabled': True,
                            'format': '{point.y:.1f}'
                        }
                    }
            },
            'tooltip': {
                'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> of total<br/>'
            },
            'series': [data]
        }

        dump = json.dumps(chart)        
        return render(request, 'indica/resago.html', {'chart': dump,'yea': yea ,'care':care,'form': form,'datos':datos, 'tipo':tipo,'fin' : fin, 'inicio' : inicio,'rango':rango, 'bandera': bandera})
    else:
        bandera = 0
    return render(request, 'indica/resago.html', {'form': form,'yea':yea, 'bandera': bandera})

#retencion son los alumnos que se incriben en primero o septimo en una fecha y se inscriben al siguentte ano en cuarto o decimo
def retencion(request):
    form = Resagoform()
    bandera = 0
    if request.method == 'POST':
        inicio =  request.POST['ain']
        fin = request.POST['afi']
        tipo = request.POST['tipo']
        carrera = request.POST['id_carrera']
        inran=int(inicio)
        firan=int(fin)
        care = Carreras.objects.get(id=carrera)
        bandera = 1
        datos=[]
        aos=[]
        #seleccioanr los datos para extraer la carrera y ver si es ingenieria o tsu
        care= Carreras.objects.get(id=carrera)
        let=str(care.nombre)[:3].lower()
        if inran>firan:
            rango = list(range(firan,inran+1))
        else:
            rango = list(range(inran,firan+1))
        if let=='ing':
            for generacion in rango:
                #calcula los alumnos que empezaron y los que estan al siguiente ano y hace los calculos para agregar a la grafica
                Alin=Movimientos.objects.filter(Q(id_tipo_movimiento=(Tipo_movimiento.objects.get(tipo='Ingreso')))|Q(id_tipo_movimiento=(Tipo_movimiento.objects.get(tipo='Reinscripcion'))), cuatrimestre=7, fecha__year=generacion,id_carrera=carrera).values_list('id_alumno',flat = True).distinct()
                Alfin=Movimientos.objects.filter(Q(id_tipo_movimiento=(Tipo_movimiento.objects.get(tipo='Ingreso')))|Q(id_tipo_movimiento=(Tipo_movimiento.objects.get(tipo='Reinscripcion'))),cuatrimestre=10, fecha__year=(generacion+1),id_carrera=carrera).values_list('id_alumno',flat = True).distinct()
                comparacion = [item for item in Alin if item in Alfin]
                gene=str(generacion)+"-"+str(generacion+1)
                aos.append(gene)
                tamal=len(comparacion)
                alint=len(Alin)
                try:    
                    tam=((tamal/alint)*100)
                except:
                    tam=0
                datos.append(tam)
        else:
            for generacion in rango:    
                #calcula los alumnos que empezaron y los que estan al siguiente ano y hace los calculos para agregar a la grafica
                Alin=Movimientos.objects.filter(Q(id_tipo_movimiento=(Tipo_movimiento.objects.get(tipo='Ingreso')))|Q(id_tipo_movimiento=(Tipo_movimiento.objects.get(tipo='Reinscripcion'))), cuatrimestre=1, fecha__year=generacion,id_carrera=carrera).values_list('id_alumno',flat = True).distinct()
                Alfin=Movimientos.objects.filter(Q(id_tipo_movimiento=(Tipo_movimiento.objects.get(tipo='Ingreso')))|Q(id_tipo_movimiento=(Tipo_movimiento.objects.get(tipo='Reinscripcion'))),cuatrimestre=4, fecha__year=(generacion+1),id_carrera=carrera).values_list('id_alumno',flat = True).distinct()
                comparacion = [item for item in Alin if item in Alfin]
                gene="Ago "+str(generacion)+" - Sep "+str(generacion+1)
                aos.append(gene)
                tamal=len(comparacion)
                alint=len(Alin)
                try:    
                    tam=((tamal/alint)*100)
                except:
                    tam=0
                datos.append(tam)
        #inicio=Alumno.objects.filter( Q(id_status_ing = (Tipo_status.objects.get(descripcion='Activo' ))) | Q(id_status_ing = (Tipo_status.objects.get(descripcion='Egresado' ))) | Q(id_status_ing = (Tipo_status.objects.get(descripcion='Titulado' ))),id_carrera_ing=int(carrera),generacion_ing=generacion)
        data = {
            'name': 'Generaciones',
            'data': datos,
        }
        chart = {
            'chart': {'type': tipo},
            'xAxis': {'categories': aos},
            'title': {'text': 'Índice de retención'},
            'subtitle':{'text': str(care)},
            'plotOptions': {
                    'series': {
                        'borderWidth': 0,
                        'dataLabels': {
                            'enabled': True,
                            'format': '{point.y:.1f}' + ' %'
                        }
                    }
            },
            'tooltip': {
                'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> %  of total<br/>'
            },
            'series': [data]
        }
    
        dump = json.dumps(chart)
        #retornar todo al formulario
        return render(request, 'indica/retencion.html',{'form':form,'chart': dump,'bandera': bandera})
    return render(request, 'indica/retencion.html',{'form':form, 'bandera': bandera})

def desersion(request):
    form = AbandonoEscolar
    hoy = datetime.date.today()
    yea = hoy.year
    bandera = 0
    if request.method == 'POST':
        carrera = request.POST['id_carrera']
        inicio =  request.POST['ain']
        fin = request.POST['afi']
        tipo = request.POST['tipo']
        inran=int(inicio)
        firan=int(fin)
        bandera = 1
        datos=[]
        pie=[]
        #se busca la carrera pare definir si es un ingenieria o un tsu
        care= Carreras.objects.get(id=carrera)
        let=str(care.nombre)[:3].lower()
        if inran>firan:
            rango = list(range(firan,inran+1))
        else:
            rango = list(range(inran,firan+1))
        
          
        if let=='ing':
            for generacion in rango:
                #calcula los alumnos que estan de baja definitiva en ingenieria y lo  agrega para graficar
                cortetsu = Movimientos.objects.filter(id_carrera=int(carrera),fecha__year=generacion).count()
                bajaDefIng = Alumno.objects.filter(id_carrera_ing=int(carrera),generacion_ing=generacion , id_status_ing = (Tipo_status.objects.get(descripcion='Baja Temporal'))).count()
                pie.append("Sep "+str(generacion)+" - Ago "+str(generacion+2))
                datos.append(int(bajaDefIng))
                
        else:
            for generacion in rango:
                #calcula los alumnos que estan de baja definitiva en tsu y lo  agrega para graficar
                cortetsu = Movimientos.objects.filter(id_carrera=int(carrera),fecha__year=generacion).count()
                bajaDeftsu = Alumno.objects.filter(id_carrera=int(carrera),generacion_tsu=generacion , id_status_tsu = (Tipo_status.objects.get(descripcion='Baja Temporal'))).count()
                datos.append(int(bajaDeftsu))
                pie.append("Sep "+str(generacion)+" - Ago "+str(generacion+2))
        data = {
            'name': 'Generaciones',
            'data': datos,
        }
        chart = {
            'chart': {'type': tipo},
            'xAxis': {'categories': pie},
            'title': {'text': 'Índice de deserción'},
            'subtitle': {'text':str(care)},
            #plotOptins indica el estilo que tendran los valores que aparecen arriba de las graficas
            'plotOptions': {
                    'series': {
                        'borderWidth': 0,
                        'dataLabels': {
                        #se coloca el atributo enabled en True para que estos valores aparezcan
                            'enabled': True,
                        #En el atributo format se delimita el formato con el cual aparecera
                            'format': '{point.y:.1f}'
                        }
                    }
            },

            'tooltip': {
                'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> of total<br/>'
            },
            'series': [data]
        }

        dump = json.dumps(chart)
        #Retornar los datos a la plantilla
        return render(request, 'indica/desercion.html', {'chart': dump,'yea':yea,'care':care,'form': form,'datos':datos, 'tipo':tipo,'fin' : fin, 'inicio' : inicio,'rango':rango, 'bandera': bandera})
    else:
        bandera = 0
    return render(request,'indica/desercion.html',{'yea':yea,'form': form, 'bandera': bandera})

def abandonoEscolar(request):
    form = AbandonoEscolar
    hoy = datetime.date.today()
    yea = hoy.year
    bandera = 0
    if request.method == 'POST':
        carrera = request.POST['id_carrera']
        inicio =  request.POST['ain']
        fin = request.POST['afi']
        tipo = request.POST['tipo']
        inran=int(inicio)
        firan=int(fin)
        bandera = 1
        datos=[]
        pie=[]
        care= Carreras.objects.get(id=carrera)
        let=str(care.nombre)[:3].lower()
        if inran>firan:
            rango = list(range(firan,inran+1))
        else:
            rango = list(range(inran,firan+1))
            
        if let=='ing':
            for generacion in rango:
                cortetsu = Movimientos.objects.filter(id_carrera=int(carrera),fecha__year=generacion).count()
                bajaDefIng = Alumno.objects.filter(id_carrera_ing=int(carrera),generacion_ing=generacion , id_status_ing = (Tipo_status.objects.get(descripcion='Baja Definitiva'))).count()
                pie.append("Sep"+str(generacion)+"-Ago"+str(generacion+2))
                datos.append(int(bajaDefIng))
                
        else:
            for generacion in rango:
                cortetsu = Movimientos.objects.filter(id_carrera=int(carrera),fecha__year=generacion).count()
                bajaDeftsu = Alumno.objects.filter(id_carrera=int(carrera),generacion_tsu=generacion , id_status_tsu = (Tipo_status.objects.get(descripcion='Baja Definitiva'))).count()
                datos.append(int(bajaDeftsu))
                pie.append("Sep"+str(generacion)+"-Ago"+str(generacion+2))
        data = {
            'name': 'Generaciones',
            'data': datos,
        }
        chart = {
            'chart': {'type': tipo},
            'xAxis': {'categories': pie},
            'title': {'text': 'Índice de abandono escolar'},
            'subtitle': {'text': str(care)},
            'plotOptions': {
                    'series': {
                        'borderWidth': 0,
                        'dataLabels': {
                            'enabled': True,
                            'format': '{point.y:.1f}'
                        }
                    }
            },
            'tooltip': {
                'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> of total<br/>'
            },
            'series': [data]
        }

        dump = json.dumps(chart)        
        return render(request, 'indica/abandono_escolar.html', {'chart': dump,'yea':yea,'care':care,'form': form,'datos':datos, 'tipo':tipo,'fin' : fin, 'inicio' : inicio,'rango':rango, 'bandera': bandera})
    else:
        bandera = 0
    return render(request, 'indica/abandono_escolar.html', {'yea':yea,'form': form, 'bandera': bandera})

def importarMov(request):  
    conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=172.16.8.44;DATABASE=sic;UID=ezt_uzu_FG;PWD=02052019')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sic.cat_movimiento_alumno')
    for row in cursor:
        m=Tipo_movimiento(tipo=row.nombre)
        m.save()
    cursor.close()
    conn.close()
    return render(request, 'importar/importarDatos.html', {})

