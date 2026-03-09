from django.shortcuts import render
from .models import Equipo

def lista_equipos(request):
    # Vamos a la base de datos y traemos TODOS los equipos
    equipos = Equipo.objects.all()
    
    # Se los enviamos a un archivo HTML (que crearemos en el siguiente paso)
    return render(request, 'inventario/lista_equipos.html', {'equipos': equipos})