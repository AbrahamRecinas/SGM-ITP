from django.contrib import admin
from .models import Equipo

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    # Las columnas que se verán en la tabla principal
    list_display = ('numero_serie', 'marca', 'modelo', 'ram', 'disco_duro', 'estado')
    # Agrega una barra de búsqueda para encontrar equipos rápido
    search_fields = ('numero_serie', 'marca', 'modelo')
    # Agrega filtros laterales (ej. ver solo los "En Mantenimiento")
    list_filter = ('estado', 'marca')