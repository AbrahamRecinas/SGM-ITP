from django import forms
from .models import ReporteFalla

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