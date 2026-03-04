from django.db import models

class Equipo(models.Model):
    # Opciones para el estado de la computadora
    ESTADO_CHOICES = [
        ('Activo', 'Activo - En uso'),
        ('Mantenimiento', 'En Mantenimiento'),
        ('Baja', 'Dado de Baja'),
    ]

    numero_serie = models.CharField(max_length=50, unique=True, verbose_name="Número de Serie")
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    procesador = models.CharField(max_length=50)
    ram = models.CharField(max_length=20, verbose_name="Memoria RAM (GB)")
    disco_duro = models.CharField(max_length=50, verbose_name="Almacenamiento (Disco Duro)", default="No especificado")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    # Esto es para que en el panel de administrador se vea el nombre bonito del equipo
    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.numero_serie})"