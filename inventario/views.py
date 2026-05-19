from django.contrib.auth.decorators import login_required, permission_required # <-- Agregamos permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Equipo, ReporteFalla, Mantenimiento, Edificio
from .forms import ReporteFallaForm, AtenderReporteForm, MantenimientoForm, EquipoForm

def lista_equipos(request):
    query = request.GET.get('q')
    edificio_id = request.GET.get('edificio') # Capturamos si seleccionaron un edificio
    
    equipos = Equipo.objects.all()
    
    # Filtro por barra de búsqueda
    if query:
        equipos = equipos.filter(
            Q(numero_serie__icontains=query) | 
            Q(marca__icontains=query) | 
            Q(modelo__icontains=query)
        )
    
    # Filtro por edificio
    if edificio_id:
        equipos = equipos.filter(edificio_id=edificio_id)
        
    # Traemos todos los edificios para el menú desplegable de la interfaz
    edificios = Edificio.objects.all()
    
    return render(request, 'inventario/lista_equipos.html', {
        'equipos': equipos, 
        'query': query,
        'edificios': edificios,
        'edificio_seleccionado': edificio_id
    })
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

# --- NUEVA VISTA PARA ATENDER REPORTES (SOLO TÉCNICOS) ---
@login_required
@permission_required('inventario.change_reportefalla', raise_exception=True)
def atender_reporte(request, reporte_id):
    # Buscamos el reporte exacto por su ID
    reporte = get_object_or_404(ReporteFalla, id=reporte_id)
    
    if request.method == 'POST':
        form = AtenderReporteForm(request.POST, instance=reporte)
        if form.is_valid():
            form.save()
            return redirect('lista_reportes')
    else:
        # Si apenas entra a la página, le mostramos el formulario pre-llenado con el estado actual
        form = AtenderReporteForm(instance=reporte)
        
    return render(request, 'inventario/atender_reporte.html', {'form': form, 'reporte': reporte})

# --- VISTA PARA REGISTRAR UN MANTENIMIENTO ---
@login_required
@permission_required('inventario.add_mantenimiento', raise_exception=True)
def registrar_mantenimiento(request):
    if request.method == 'POST':
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            # Magia de Django: Pausamos el guardado (commit=False)
            mantenimiento = form.save(commit=False)
            # Le inyectamos a la fuerza el estado Terminado
            mantenimiento.estado_mantenimiento = 'Terminado'
            # Ahora sí, guardamos en la base de datos
            mantenimiento.save()
            
            return redirect('lista_mantenimientos')
    else:
        form = MantenimientoForm()
        
    return render(request, 'inventario/registrar_mantenimiento.html', {'form': form})

@login_required
@permission_required('inventario.add_equipo', raise_exception=True)
def nuevo_equipo(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_equipos')
    else:
        form = EquipoForm()
    return render(request, 'inventario/nuevo_equipo.html', {'form': form})

@login_required
@permission_required('inventario.change_equipo', raise_exception=True)
def editar_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    
    if request.method == 'POST':
        # Le pasamos instance=equipo para que Django sepa que va a EDITAR este registro, no a crear uno nuevo
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect('lista_equipos')
    else:
        form = EquipoForm(instance=equipo)
        
    return render(request, 'inventario/editar_equipo.html', {'form': form, 'equipo': equipo})