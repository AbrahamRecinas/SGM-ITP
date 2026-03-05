from django.db import models

# 1. NUEVA TABLA: Jerarquía de Edificios
class Edificio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Edificio/Área")
    
    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo - En uso'),
        ('Mantenimiento', 'En Mantenimiento'),
        ('Baja', 'Dado de Baja'),
    ]

    # Conectamos el equipo a un edificio (null=True evita errores si ya tenías equipos guardados)
    edificio = models.ForeignKey(Edificio, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ubicación (Edificio)")
    
    numero_serie = models.CharField(max_length=50, unique=True, verbose_name="Número de Serie")
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    procesador = models.CharField(max_length=50)
    ram = models.CharField(max_length=20, verbose_name="Memoria RAM (GB)")
    disco_duro = models.CharField(max_length=50, verbose_name="Almacenamiento (Disco Duro)", default="No especificado")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.numero_serie})"

# 2. MEJORA DE ESTADOS: Reportes
class ReporteFalla(models.Model):
    ESTADO_REPORTE = [
        ('Pendiente', 'Pendiente de revisión'),
        ('En Revision', 'En revisión por CC'), # Nuevo estado intermedio
        ('Finalizado', 'Mantenimiento finalizado'),
    ]

    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, verbose_name="Equipo que falla")
    fecha_reporte = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora del Reporte")
    solicitante = models.CharField(max_length=100, verbose_name="¿Quién reporta?")
    descripcion_falla = models.TextField(verbose_name="Descripción del problema")
    estado = models.CharField(max_length=20, choices=ESTADO_REPORTE, default='Pendiente')

    def __str__(self):
        return f"Reporte: {self.equipo.numero_serie} - {self.estado}"

# 3. EL CEREBRO: Mantenimiento con reacción en cadena
class Mantenimiento(models.Model):
    TIPO_CHOICES = [
        ('Preventivo', 'Preventivo (Limpieza)'),
        ('Correctivo', 'Correctivo (Falla)'),
    ]
    ESTADO_MANTENIMIENTO_CHOICES = [
        ('Pendiente', 'Pendiente por revisar'),
        ('En curso', 'Trabajando en el equipo'),
        ('Terminado', 'Mantenimiento finalizado'),
    ]

    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, verbose_name="Equipo")
    
    # NUEVO: Conectamos el mantenimiento al reporte original (opcional, porque a veces hay mantenimientos sin reporte)
    reporte_vinculado = models.ForeignKey(ReporteFalla, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Reporte Asociado")
    
    fecha = models.DateField(verbose_name="Fecha del Mantenimiento")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='Preventivo')
    estado_mantenimiento = models.CharField(max_length=20, choices=ESTADO_MANTENIMIENTO_CHOICES, default='Pendiente', verbose_name="Estado del Mantenimiento")
    descripcion = models.TextField(verbose_name="Descripción del trabajo")
    tecnico = models.CharField(max_length=100, verbose_name="Técnico (CC)")

    # EL EFECTO DOMINÓ
    def save(self, *args, **kwargs):
        if self.estado_mantenimiento in ['Pendiente', 'En curso']:
            self.equipo.estado = 'Mantenimiento'
            # Si hay un reporte vinculado, le avisamos al edificio que ya lo estamos viendo
            if self.reporte_vinculado:
                self.reporte_vinculado.estado = 'En Revision'
                self.reporte_vinculado.save()
                
        elif self.estado_mantenimiento == 'Terminado':
            self.equipo.estado = 'Activo'
            # Si hay reporte, lo cerramos
            if self.reporte_vinculado:
                self.reporte_vinculado.estado = 'Finalizado'
                self.reporte_vinculado.save()
                
        self.equipo.save() 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} - {self.equipo.numero_serie}"

#HOLA ABRAHAM SOY ERICK, YA VINE A SOLUIONAR EL PROGRAMA, YA NO HAY DE QUE PREOCUPARSE PUES ESTOY AQUI.