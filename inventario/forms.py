from django import forms
from .models import ReporteFalla, Mantenimiento, Equipo # <-- Agregamos los que faltaban
        
class AtenderReporteForm(forms.ModelForm):
    class Meta:
        model = ReporteFalla
        fields = ['estado'] # Solo dejamos que editen el estado
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
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


class ReporteFallaForm(forms.ModelForm):
    class Meta:
        model = ReporteFalla
        fields = ['equipo', 'descripcion_falla'] # Adiós solicitante, se llena solo en la vista
        widgets = {
            'equipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_falla': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        if usuario and hasattr(usuario, 'perfil'):
            self.fields['equipo'].queryset = Equipo.objects.filter(edificio=usuario.perfil.edificio)


class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        # ¡Solo pedimos estos 3! Todo lo demás (fecha, técnico, reporte) lo inyecta la vista
        fields = ['equipo', 'tipo', 'descripcion']
        
        widgets = {
            'equipo': forms.Select(attrs={'class': 'form-select', 'id': 'id_equipo'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '¿Qué se le hizo al equipo?'}),
        }