from django.contrib import admin
from .models import Equipo, Mantenimiento

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    # Las columnas que se verán en la tabla principal
    list_display = ('numero_serie', 'marca', 'modelo', 'ram', 'disco_duro', 'estado')
    # Agrega una barra de búsqueda para encontrar equipos rápido
    search_fields = ('numero_serie', 'marca', 'modelo')
    # Agrega filtros laterales (ej. ver solo los "En Mantenimiento")
    list_filter = ('estado', 'marca')

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    # Agregamos el estado_mantenimiento a la vista
    list_display = ('equipo', 'fecha', 'tipo', 'estado_mantenimiento', 'tecnico')
    list_filter = ('tipo', 'estado_mantenimiento', 'fecha')
    search_fields = ('equipo__numero_serie', 'tecnico')