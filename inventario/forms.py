from django import forms
from .models import ReporteFalla, Mantenimiento, Equipo # <-- Agregamos los que faltaban

class ReporteFallaForm(forms.ModelForm):
    class Meta:
        model = ReporteFalla
        # Solo pedimos los datos que el usuario necesita llenar. 
        # (La fecha y el estado se ponen solos, ¿recuerdas?)
        fields = ['equipo', 'solicitante', 'descripcion_falla']
        
        # Le ponemos el diseño moderno de Bootstrap a las casillas
        widgets = {
            'equipo': forms.Select(attrs={'class': 'form-select'}),
            'solicitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan Pérez - Edificio A'}),
            'descripcion_falla': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe detalladamente el problema...'}),
        }
        
class AtenderReporteForm(forms.ModelForm):
    class Meta:
        model = ReporteFalla
        fields = ['estado'] # Solo dejamos que editen el estado
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        # ¡Agregamos 'reporte_vinculado' a la lista!
        fields = ['equipo', 'reporte_vinculado', 'fecha', 'tipo', 'descripcion', 'tecnico']
        
        widgets = {
            'equipo': forms.Select(attrs={'class': 'form-select'}),
            # Le ponemos el diseño bonito al nuevo campo
            'reporte_vinculado': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '¿Qué se le hizo al equipo?'}),
            'tecnico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del técnico (Ej. Abraham o Erick)'}),
        }

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        # Agregamos 'sistema_operativo' a la lista
        fields = ['edificio', 'numero_serie', 'marca', 'modelo', 'sistema_operativo', 'procesador', 'ram', 'disco_duro', 'estado']
        
        widgets = {
            'edificio': forms.Select(attrs={'class': 'form-select'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de serie único'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. HP, Dell, Asus'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. ThinkPad, Latitude'}),
            # Nuevo selector para el OS
            'sistema_operativo': forms.Select(attrs={'class': 'form-select'}),
            'procesador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Intel Core i5 / Ryzen 5'}),
            'ram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 8GB, 16GB'}),
            'disco_duro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. SSD 512GB / HDD 1TB'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }