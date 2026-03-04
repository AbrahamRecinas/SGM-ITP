from django.contrib import admin
from .models import Edificio, Equipo, Mantenimiento, ReporteFalla

# 1. Registramos los Edificios
@admin.register(Edificio)
class EdificioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# 2. Actualizamos los Equipos (ahora muestran su Edificio)
@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('numero_serie', 'marca', 'modelo', 'ram', 'disco_duro', 'edificio', 'estado')
    search_fields = ('numero_serie', 'marca', 'modelo')
    # Agregamos 'edificio' al filtro lateral para encontrar máquinas por zona
    list_filter = ('estado', 'edificio', 'marca') 

# 3. Actualizamos los Reportes
@admin.register(ReporteFalla)
class ReporteFallaAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'solicitante', 'fecha_reporte', 'estado')
    # Un truco pro: filtramos los reportes basándonos en el edificio del equipo
    list_filter = ('estado', 'equipo__edificio', 'fecha_reporte')
    search_fields = ('equipo__numero_serie', 'solicitante', 'descripcion_falla')

# 4. Actualizamos los Mantenimientos (ahora muestran si nacieron de un Reporte)
@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'fecha', 'tipo', 'estado_mantenimiento', 'tecnico', 'reporte_vinculado')
    list_filter = ('tipo', 'estado_mantenimiento', 'fecha')
    search_fields = ('equipo__numero_serie', 'tecnico')