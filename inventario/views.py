from django.contrib.auth.decorators import login_required, permission_required # <-- Agregamos permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .models import Equipo, ReporteFalla, Mantenimiento, Edificio
from .forms import ReporteFallaForm, AtenderReporteForm, MantenimientoForm, EquipoForm
from django.urls import reverse
@login_required
def lista_equipos(request):
    query = request.GET.get('q')
    edificio_id = request.GET.get('edificio')
    
    # 1. Traemos los equipos
    equipos = Equipo.objects.all()
    
    # 2. AISLAMIENTO: Si es Admin de edificio, filtramos a la fuerza
    if hasattr(request.user, 'perfil'):
        equipos = equipos.filter(edificio=request.user.perfil.edificio)
    else:
        # Solo si es técnico aplicamos el filtro del menú desplegable
        if edificio_id:
            equipos = equipos.filter(edificio_id=edificio_id)
    
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

def lista_mantenimientos(request):
    # Traemos los mantenimientos ordenados del más reciente al más antiguo
    mantenimientos = Mantenimiento.objects.all().order_by('-fecha')
    return render(request, 'inventario/lista_mantenimientos.html', {'mantenimientos': mantenimientos})

@login_required
def nuevo_reporte(request):
    if request.method == 'POST':
        # Le pasamos el usuario al formulario
        form = ReporteFallaForm(request.POST, usuario=request.user)
        if form.is_valid():
            reporte = form.save(commit=False)
            
            reporte.solicitante = request.user
                
            reporte.save()
            return redirect('lista_reportes')
    else:
        # MAGIA: Atrapamos el ID si venimos del escáner QR
        equipo_id = request.GET.get('equipo_id')
        
        if equipo_id:
            # Le pasamos el usuario y PRE-LLENAMOS el equipo
            form = ReporteFallaForm(usuario=request.user, initial={'equipo': equipo_id})
        else:
            # Le pasamos el usuario al formulario vacío (flujo normal)
            form = ReporteFallaForm(usuario=request.user)
        
    return render(request, 'inventario/nuevo_reporte.html', {'form': form})

# --- VISTA DE DETALLE CON QR ---
@login_required
def detalle_equipo(request, equipo_id):
    # Esta función busca el equipo por su ID, si no existe muestra un error 404
    equipo = get_object_or_404(Equipo, id=equipo_id)
    
    # Buscamos los últimos 5 reportes de este equipo específico
    reportes = ReporteFalla.objects.filter(equipo=equipo).order_by('-fecha_reporte')[:5]
    # NUEVO: Traemos todo el historial médico de esta PC
    mantenimientos = Mantenimiento.objects.filter(equipo=equipo).order_by('-fecha')
    
    return render(request, 'inventario/detalle_equipo.html', {
        'equipo': equipo,
        'reportes': reportes,
        'mantenimientos': mantenimientos
    })

# --- NUEVA VISTA PARA ATENDER REPORTES (SOLO TÉCNICOS) ---
@login_required
@permission_required('inventario.change_reportefalla', raise_exception=True)
def atender_reporte(request, reporte_id):
    reporte = get_object_or_404(ReporteFalla, id=reporte_id)
    
    # Al presionar "Recibir e Iniciar Revisión"
    if request.method == 'POST' and 'iniciar_revision' in request.POST:
        reporte.estado = 'En Revision'
        reporte.equipo.estado = 'Mantenimiento'  # Bloqueamos el equipo en el catálogo
        reporte.equipo.save()
        reporte.save()
        return redirect('lista_reportes')
        
    return render(request, 'inventario/atender_reporte.html', {'reporte': reporte})

# --- VISTA PARA REGISTRAR UN MANTENIMIENTO ---
@login_required
@permission_required('inventario.add_mantenimiento', raise_exception=True)
@login_required
def registrar_mantenimiento(request):
    reporte_id = request.GET.get('reporte_id')
    # NUEVO: Atrapamos el ID del equipo si venimos del escáner QR directo
    equipo_id = request.GET.get('equipo_id')
    
    reporte = None
    datos_iniciales = {}

    # Si venimos desde un reporte (Efecto Dominó de Erick)
    if reporte_id:
        reporte = get_object_or_404(ReporteFalla, id=reporte_id)
        datos_iniciales['equipo'] = reporte.equipo
        datos_iniciales['tipo'] = 'Correctivo'
    
    # NUEVO: Si venimos desde el escáner QR de mantenimientos
    elif equipo_id:
        # Buscamos la máquina para asegurar que exista y pre-llenamos el campo
        equipo = get_object_or_404(Equipo, id=equipo_id)
        datos_iniciales['equipo'] = equipo
        # Podemos dejar el tipo vacío o sugerir 'Preventivo' por defecto si es de rutina
        datos_iniciales['tipo'] = 'Preventivo' 

    if request.method == 'POST':
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            mantenimiento = form.save(commit=False)
            
            # Autocompletado silencioso
            mantenimiento.tecnico = request.user
            mantenimiento.estado_mantenimiento = 'Terminado'
            mantenimiento.fecha = timezone.now()
            
            if reporte_id:
                reporte = get_object_or_404(ReporteFalla, id=reporte_id)
                mantenimiento.reporte_vinculado = reporte
                mantenimiento.save() 
                return redirect('lista_reportes') 
            else:
                mantenimiento.save()
                return redirect('lista_mantenimientos')       
    else:
        form = MantenimientoForm(initial=datos_iniciales)

    return render(request, 'inventario/registrar_mantenimiento.html', {'form': form, 'reporte': reporte})

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

@login_required
def lista_reportes(request):
    query = request.GET.get('q')
    estado_filtro = request.GET.get('estado')
    
    reportes = ReporteFalla.objects.all().order_by('-fecha_reporte')
    
    # 1. AISLAMIENTO: Si es Admin de Edificio, solo ve los de su edificio
    if hasattr(request.user, 'perfil'):
        reportes = reportes.filter(equipo__edificio=request.user.perfil.edificio)

    # 2. BÚSQUEDA (Folio, Solicitante o Serie del equipo)
    if query:
        reportes = reportes.filter(
            Q(folio__icontains=query) |
            Q(solicitante__username__icontains=query) | # Buscamos por nombre de usuario
            Q(equipo__numero_serie__icontains=query)
        )
        
    # 3. FILTRO POR ESTADO
    if estado_filtro:
        reportes = reportes.filter(estado=estado_filtro)
        
    return render(request, 'inventario/lista_reportes.html', {
        'reportes': reportes,
        'query': query,
        'estado_filtro': estado_filtro
    })

@login_required
def dashboard(request):
    # 1. Contadores base
    total_equipos = Equipo.objects.count()
    equipos_mantenimiento = Equipo.objects.filter(estado='Mantenimiento').count()
    
    # 2. RBAC: Si es Admin de Edificio, las métricas son solo de su zona
    if hasattr(request.user, 'perfil'):
        edificio_usuario = request.user.perfil.edificio
        total_equipos = Equipo.objects.filter(edificio=edificio_usuario).count()
        equipos_mantenimiento = Equipo.objects.filter(edificio=edificio_usuario, estado='Mantenimiento').count()
        reportes_pendientes = ReporteFalla.objects.filter(equipo__edificio=edificio_usuario, estado='Pendiente').count()
    else:
        # Si es Técnico, ve las métricas de todo el ITP
        reportes_pendientes = ReporteFalla.objects.filter(estado='Pendiente').count()

    contexto = {
        'total_equipos': total_equipos,
        'equipos_mantenimiento': equipos_mantenimiento,
        'reportes_pendientes': reportes_pendientes,
    }
    
    return render(request, 'inventario/dashboard.html', contexto)

@login_required
def imprimir_etiquetas(request):
    equipos = Equipo.objects.all().order_by('edificio', 'numero_serie')
    
    # Aislamiento: El Admin de Edificio solo ve sus propias computadoras
    if hasattr(request.user, 'perfil'):
        equipos = equipos.filter(edificio=request.user.perfil.edificio)
        
    # NUEVO: Si entramos desde el botón de un equipo específico, filtramos solo ese
    equipo_id = request.GET.get('equipo_id')
    if equipo_id:
        equipos = equipos.filter(id=equipo_id)
        
    return render(request, 'inventario/imprimir_etiquetas.html', {'equipos': equipos})

from django.contrib import messages
from django.shortcuts import redirect

@login_required
def abrir_escaner(request):
    # 'origen' nos dirá de qué botón viene el usuario (detalle, reporte, mantenimiento)
    origen = request.GET.get('origen', 'detalle')
    return render(request, 'inventario/escaner_qr.html', {'origen': origen})

@login_required
def procesar_qr(request):
    numero_serie = request.GET.get('serie')
    origen = request.GET.get('origen', 'detalle')

    if not numero_serie:
        messages.error(request, "No se detectó ningún código.")
        return redirect('dashboard')

    # Buscamos la computadora por su número de serie
    equipo = Equipo.objects.filter(numero_serie=numero_serie).first()

    if not equipo:
        messages.warning(request, f"No se encontró ningún equipo con la serie: {numero_serie}")
        return redirect('dashboard')

    # MAGIA: Redirección según el contexto
    if origen == 'reporte':
        # Construimos la URL: /reportes/nuevo/?equipo_id=5
        url_reporte = reverse('nuevo_reporte')
        return redirect(f"{url_reporte}?equipo_id={equipo.id}") 
        
    elif origen == 'mantenimiento':
        url_mantenimiento = reverse('registrar_mantenimiento')
        return redirect(f"{url_mantenimiento}?equipo_id={equipo.id}")
        
    else:
        # Por defecto, te manda a ver la ficha técnica (desde el celular)
        return redirect('detalle_equipo', equipo_id=equipo.id)
    
