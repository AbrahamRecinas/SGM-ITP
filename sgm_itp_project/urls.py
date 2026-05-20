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
    path('equipos/<int:equipo_id>/', views.detalle_equipo, name='detalle_equipo'),
    path('equipos/', views.lista_equipos, name='lista_equipos'),
    path('reportes/', views.lista_reportes, name='lista_reportes'),
    path('reportes/nuevo/', views.nuevo_reporte, name='nuevo_reporte'),
    path('mantenimientos/', views.lista_mantenimientos, name='lista_mantenimientos'),
    path('reportes/<int:reporte_id>/atender/', views.atender_reporte, name='atender_reporte'),
    path('mantenimientos/nuevo/', views.registrar_mantenimiento, name='registrar_mantenimiento'),
    path('equipos/nuevo/', views.nuevo_equipo, name='nuevo_equipo'),
    path('equipos/<int:equipo_id>/editar/', views.editar_equipo, name='editar_equipo'),
    path('', views.dashboard, name='dashboard'),
    path('equipos/etiquetas/', views.imprimir_etiquetas, name='imprimir_etiquetas'),
    path('escaner/', views.abrir_escaner, name='abrir_escaner'),
    path('procesar-qr/', views.procesar_qr, name='procesar_qr'),
]