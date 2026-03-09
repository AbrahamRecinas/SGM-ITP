from django.shortcuts import render, redirect
from .models import Equipo, ReporteFalla, Mantenimiento
from .forms import ReporteFallaForm

def lista_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'inventario/lista_equipos.html', {'equipos': equipos})
# --- NUEVA VISTA ---
def lista_reportes(request):
    # order_by('-fecha_reporte') hace que los reportes más nuevos salgan hasta arriba
    reportes = ReporteFalla.objects.all().order_by('-fecha_reporte')
    return render(request, 'inventario/lista_reportes.html', {'reportes': reportes})
def lista_mantenimientos(request):
    # Traemos los mantenimientos ordenados del más reciente al más antiguo
    mantenimientos = Mantenimiento.objects.all().order_by('-fecha')
    return render(request, 'inventario/lista_mantenimientos.html', {'mantenimientos': mantenimientos})
def nuevo_reporte(request):
    # Si el usuario le dio clic al botón de "Guardar" (envió datos)
    if request.method == 'POST':
        form = ReporteFallaForm(request.POST)
        if form.is_valid():
            form.save() # ¡Aquí ocurre la magia! Se guarda en la base de datos
            return redirect('lista_reportes') # Lo mandamos a ver la tabla para que vea su reporte
    else:
        # Si apenas entró a la página, le mostramos el formulario en blanco
        form = ReporteFallaForm()
    
    return render(request, 'inventario/nuevo_reporte.html', {'form': form})