"""
URL configuration for sgm_itp_project project.
"""
from django.contrib import admin
from django.urls import path, include  # <-- Tu importación perfecta
from inventario import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- LA LÍNEA MÁGICA DE SEGURIDAD ---
    # Esto enciende automáticamente las rutas de login, logout, cambiar contraseña, etc.
    path('cuentas/', include('django.contrib.auth.urls')), 
    
    path('equipos/', views.lista_equipos, name='lista_equipos'),
    path('reportes/', views.lista_reportes, name='lista_reportes'),
    path('reportes/nuevo/', views.nuevo_reporte, name='nuevo_reporte'),
    path('mantenimientos/', views.lista_mantenimientos, name='lista_mantenimientos'),
]