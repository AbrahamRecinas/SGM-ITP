from django.contrib import admin
from .models import Edificio, Equipo, Mantenimiento, ReporteFalla, PerfilUsuario

# 1. Registramos los Edificios
@admin.register(Edificio)
class EdificioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# 2. Actualizamos los Equipos
@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('numero_serie', 'marca', 'modelo', 'ram', 'disco_duro', 'edificio', 'estado')
    search_fields = ('numero_serie', 'marca', 'modelo')
    list_filter = ('estado', 'edificio', 'marca') 

# 3. Actualizamos los Reportes
@admin.register(ReporteFalla)
class ReporteFallaAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'solicitante', 'fecha_reporte', 'estado')
    list_filter = ('estado', 'equipo__edificio', 'fecha_reporte')
    search_fields = ('equipo__numero_serie', 'solicitante__username', 'descripcion_falla')

# 4. Actualizamos los Mantenimientos
@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'fecha', 'tipo', 'estado_mantenimiento', 'tecnico', 'reporte_vinculado')
    list_filter = ('tipo', 'estado_mantenimiento', 'fecha')
    search_fields = ('equipo__numero_serie', 'tecnico')

# 5. NUEVO: Registramos los Perfiles de Usuario (Administradores de Edificio)
@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    # Mostramos el usuario de Django y el edificio que controla
    list_display = ('user', 'edificio')
    # Permitimos filtrar la lista por edificio
    list_filter = ('edificio',)
    # Permitimos buscar por el nombre de usuario o por el nombre del edificio
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'edificio__nombre')