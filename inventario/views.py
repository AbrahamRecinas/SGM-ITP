from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404 # <--- Importante: agregamos get_object_or_404
from .models import Equipo, ReporteFalla, Mantenimiento
from .forms import ReporteFallaForm

def lista_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'inventario/lista_equipos.html', {'equipos': equipos})

def lista_reportes(request):
    # order_by('-fecha_reporte') hace que los reportes más nuevos salgan hasta arriba
    reportes = ReporteFalla.objects.all().order_by('-fecha_reporte')
    return render(request, 'inventario/lista_reportes.html', {'reportes': reportes})

def lista_mantenimientos(request):
    # Traemos los mantenimientos ordenados del más reciente al más antiguo
    mantenimientos = Mantenimiento.objects.all().order_by('-fecha')
    return render(request, 'inventario/lista_mantenimientos.html', {'mantenimientos': mantenimientos})

@login_required
def nuevo_reporte(request):
    if request.method == 'POST':
        form = ReporteFallaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_reportes')
    else:
        form = ReporteFallaForm()
    
    return render(request, 'inventario/nuevo_reporte.html', {'form': form})

# --- VISTA DE DETALLE CON QR ---
@login_required
def detalle_equipo(request, equipo_id):
    # Esta función busca el equipo por su ID, si no existe muestra un error 404
    equipo = get_object_or_404(Equipo, id=equipo_id)
    
    # Buscamos los últimos 5 reportes de este equipo específico
    reportes = ReporteFalla.objects.filter(equipo=equipo).order_by('-fecha_reporte')[:5]
    
    return render(request, 'inventario/detalle_equipo.html', {
        'equipo': equipo,
        'reportes': reportes
    })