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
    

class Mantenimiento(models.Model):
    TIPO_CHOICES = [
        ('Preventivo', 'Preventivo (Limpieza, actualización)'),
        ('Correctivo', 'Correctivo (Reparación de falla)'),
    ]
    
    # NUEVO: Opciones para saber en qué etapa va el trabajo
    ESTADO_MANTENIMIENTO_CHOICES = [
        ('Pendiente', 'Pendiente por revisar'),
        ('En curso', 'Trabajando en el equipo'),
        ('Terminado', 'Mantenimiento finalizado'),
    ]

    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, verbose_name="Equipo")
    fecha = models.DateField(verbose_name="Fecha del Mantenimiento")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='Preventivo')
    
    # NUEVO: Campo para el estado del mantenimiento
    estado_mantenimiento = models.CharField(max_length=20, choices=ESTADO_MANTENIMIENTO_CHOICES, default='Pendiente', verbose_name="Estado del Mantenimiento")
    
    descripcion = models.TextField(verbose_name="Descripción del trabajo realizado")
    tecnico = models.CharField(max_length=100, verbose_name="Técnico que realizó el trabajo")

    # LA MAGIA: Interceptamos el momento de guardar para automatizar el equipo
    def save(self, *args, **kwargs):
        # Si el mantenimiento empieza o está en espera, el equipo pasa a "Mantenimiento"
        if self.estado_mantenimiento in ['Pendiente', 'En curso']:
            self.equipo.estado = 'Mantenimiento'
        # Si ya se terminó, el equipo vuelve a estar "Activo"
        elif self.estado_mantenimiento == 'Terminado':
            self.equipo.estado = 'Activo'
            
        self.equipo.save()  # Guardamos el cambio en el equipo
        super().save(*args, **kwargs)  # Guardamos el mantenimiento normalmente

    def __str__(self):
        return f"{self.tipo} - {self.equipo.numero_serie} ({self.estado_mantenimiento})"