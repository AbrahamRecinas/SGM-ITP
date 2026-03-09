from django.shortcuts import render
from .models import Equipo, ReporteFalla, Mantenimiento

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