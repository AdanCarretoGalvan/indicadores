function openCity(evt, cityName) {
        var i, tabcontent, tablinks;
        var band = document.getElementById('id_band');
        tabcontent = document.getElementsByClassName("tabcontent");
          for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
          }
          tablinks = document.getElementsByClassName("tablinks");
          for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
          } 
            if (band.value == 1){
                document.getElementById('titulo').hidden = true;
                document.getElementById('grafica').style.display = "block"; //contenido
                document.getElementById('id_grafica').className += ' active'; //boton
                
                band.value = 0;
            }else{
               
                document.getElementById(cityName).style.display = "block";
                evt.currentTarget.className += " active";
                document.getElementById('titulo').hidden = true;
            }
            if (evt.currentTarget.id == 'id_datos'){
                document.getElementById('titulo').hidden = false;
                asigna();
            }
        }
function asigna(){ 
        var ic = sessionStorage.getItem('idC');
        var tg = sessionStorage.getItem('grafica');
        var ai = sessionStorage.getItem('inio');
        var af = sessionStorage.getItem('fin');
        document.formulario.id_carrera.selectedIndex = ic;
        document.formulario.tipo.selectedIndex = tg;
        document.formulario.afi.value = af;


    }
