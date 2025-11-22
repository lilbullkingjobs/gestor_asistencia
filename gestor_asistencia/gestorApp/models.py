from django.db import models

# ============================================
# MODELOS BASE DEL SISTEMA
# ============================================

class Usuario(models.Model):
    """
    Modelo base de usuarios del sistema.
    Usado en: Sprint 1 (HU1, HU11), Sprint 3 (HU15, HU16)
    """
    ROLES = [
        ('alumno', 'Alumno'),
        ('apoderado', 'Apoderado'),
        ('profesor', 'Profesor'),
        ('inspector', 'Inspector'),
        ('director', 'Director'),
    ]
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)  # Sprint 3: Hasheo con make_password
    rol = models.CharField(max_length=20, choices=ROLES)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


# ============================================
# SPRINT 1: REGISTRO DE USUARIOS (15 PH)
# ============================================

class Director(models.Model):
    """
    Sprint 1 - Relación con inspectores y profesores
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    oficina = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.usuario.nombre

    class Meta:
        verbose_name = "Director"
        verbose_name_plural = "Directores"


class Profesor(models.Model):
    """
    Sprint 1 - HU1: Necesario para asignar cursos
    Sprint 7 - HU18: Panel de control profesor
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    oficina = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.usuario.nombre

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"


class Curso(models.Model):
    """
    Sprint 1 - HU1: Registro de alumno requiere curso
    Sprint 2 - HU2: Marcaje por curso
    """
    nombre = models.CharField(max_length=100)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['nombre']


class Apoderado(models.Model):
    """
    Sprint 1 - HU1: Registro de alumno con apoderado
    Sprint 4 - HU4: Portal de apoderado
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.usuario.nombre

    class Meta:
        verbose_name = "Apoderado"
        verbose_name_plural = "Apoderados"


class Alumno(models.Model):
    """
    Sprint 1 - HU1: Registro de alumno (8 PH)
    Sprint 2 - HU2, HU3: Asistencia y retiro
    Sprint 4 - HU5: Historial de asistencia
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, unique=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.usuario.nombre

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"
        ordering = ['usuario__nombre']


class Inspector(models.Model):
    """
    Sprint 1 - HU11: Registrar apoderado e inspectores (7 PH)
    Sprint 2 - HU2, HU3: Marcar asistencia y retiro
    Sprint 4 - HU17, HU14: Notificaciones
    Sprint 7 - HU18: Panel de control inspector
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    turno = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario.nombre

    class Meta:
        verbose_name = "Inspector"
        verbose_name_plural = "Inspectores"


# ============================================
# SPRINT 2: ASISTENCIA Y RETIRO (16 PH)
# ============================================

class Asistencia(models.Model):
    """
    Sprint 2 - HU2: Marcar asistencia (10 PH)
    Sprint 2 - HU3: Retiro durante jornada (6 PH)
    Sprint 4 - HU5: Visualizar historial
    Sprint 5 - HU7, HU8: Notificaciones y monitoreo
    Sprint 6 - HU10, HU13: Reportes
    Sprint 7 - HU12: Modificar asistencia manualmente (13 PH)
    """
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField(auto_now_add=True)
    hora_ingreso = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[
        ('Presente', 'Presente'),
        ('Ausente', 'Ausente'),
        ('Retirado', 'Retirado')
    ], default='Ausente')
    observacion = models.TextField(blank=True, null=True)
    autorizado_por = models.ForeignKey(
        Apoderado, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='retiros_autorizados'
    )

    def __str__(self):
        return f"{self.alumno.usuario.nombre} - {self.fecha} - {self.estado}"

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        ordering = ['-fecha', 'alumno__usuario__nombre']
        indexes = [
            models.Index(fields=['fecha', 'estado']),
            models.Index(fields=['alumno', 'fecha']),
        ]


# ============================================
# SPRINT 5: CERTIFICADOS Y MONITOREO (29 PH)
# ============================================

class CertificadoMedico(models.Model):
    """
    Sprint 5 - HU6: Subir certificado médico (12 PH)
    Sprint 6 - HU9: Validar certificados médicos (11 PH)
    """
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='certificados')
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE, related_name='certificados_subidos')
    fecha_emision = models.DateField()
    motivo = models.TextField()
    archivo_pdf = models.FileField(upload_to='certificados/')
    validado = models.BooleanField(default=False)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificado de {self.alumno.usuario.nombre} - {self.fecha_emision}"

    class Meta:
        verbose_name = "Certificado Médico"
        verbose_name_plural = "Certificados Médicos"
        ordering = ['-fecha_subida']


# ============================================
# SPRINT 4: PORTAL APODERADO Y NOTIFICACIONES (29 PH)
# ============================================

class Notificacion(models.Model):
    """
    Sprint 4 - HU4: Acceso al portal de apoderado (9 PH)
    Sprint 4 - HU17: Notificación de atraso (6 PH)
    Sprint 4 - HU14: Alerta por inasistencia prolongada (6 PH)
    Sprint 5 - HU7: Notificación de inasistencia (7 PH)
    """
    TIPOS_NOTIFICACION = [
        ('Atraso', 'Atraso'),
        ('Inasistencia', 'Inasistencia'),
        ('Inasistencia Prolongada', 'Inasistencia Prolongada'),
        ('Certificado Médico', 'Certificado Médico'),
        ('Certificado Validado', 'Certificado Validado'),
        ('Certificado Rechazado', 'Certificado Rechazado'),
        ('Retiro', 'Retiro'),
        ('General', 'General'),
    ]
    
    tipo = models.CharField(max_length=50, choices=TIPOS_NOTIFICACION)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='notificaciones')
    inspector = models.ForeignKey(
        Inspector, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='notificaciones_enviadas'
    )
    apoderado = models.ForeignKey(
        Apoderado, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='notificaciones_recibidas'
    )
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificación {self.tipo} - {self.alumno.usuario.nombre}"

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-fecha_envio']
        indexes = [
            models.Index(fields=['-fecha_envio']),
            models.Index(fields=['apoderado', '-fecha_envio']),
        ]


# ============================================
# SPRINT 8: EXPORTACIÓN Y AUDITORÍA (21 PH)
# ============================================

class Auditoria(models.Model):
    """
    Sprint 8 - HU20: Registro de auditoría (13 PH)
    
    Registra todas las acciones críticas del sistema:
    - Modificaciones de asistencia (HU12)
    - Exportación de reportes (HU19)
    - Validación de certificados (HU9)
    - Cambios de contraseña (HU16)
    - Acciones administrativas
    """
    ACCIONES = [
        ('Login', 'Inicio de Sesión'),
        ('Logout', 'Cierre de Sesión'),
        ('Registro Usuario', 'Registro de Usuario'),
        ('Modificación de Asistencia', 'Modificación de Asistencia'),
        ('Exportación de Reporte', 'Exportación de Reporte'),
        ('Validación Certificado', 'Validación de Certificado'),
        ('Rechazo Certificado', 'Rechazo de Certificado'),
        ('Cambio Contraseña', 'Cambio de Contraseña'),
        ('Envío Notificación', 'Envío de Notificación'),
        ('Otro', 'Otra Acción'),
    ]
    
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='auditorias',
        help_text="Usuario que realizó la acción"
    )
    accion = models.CharField(
        max_length=100,
        choices=ACCIONES,
        help_text="Tipo de acción realizada"
    )
    detalle = models.TextField(help_text="Descripción detallada de la acción")
    tabla_afectada = models.CharField(
        max_length=50, 
        help_text="Tabla o modelo afectado"
    )
    registro_id = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="ID del registro modificado"
    )
    fecha_hora = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(
        null=True, 
        blank=True, 
        help_text="Dirección IP del usuario"
    )

    def __str__(self):
        return f"{self.usuario.nombre} - {self.accion} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        verbose_name = "Auditoría"
        verbose_name_plural = "Auditorías"
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['-fecha_hora']),
            models.Index(fields=['usuario', '-fecha_hora']),
            models.Index(fields=['tabla_afectada']),
            models.Index(fields=['accion']),
        ]


# ============================================
# RESUMEN DE MODELOS POR SPRINT
# ============================================
"""
SPRINT 1 (15 PH):
- Usuario (base)
- Director
- Profesor
- Curso
- Apoderado
- Alumno
- Inspector

SPRINT 2 (16 PH):
- Asistencia (HU2, HU3)

SPRINT 3 (19 PH):
- Usuario.contrasena con hasheo (HU15, HU16)

SPRINT 4 (29 PH):
- Notificacion (HU4, HU17, HU14)

SPRINT 5 (29 PH):
- CertificadoMedico (HU6, HU7, HU8)

SPRINT 6 (28 PH):
- Uso de modelos existentes para reportes (HU9, HU10, HU13)

SPRINT 7 (25 PH):
- Asistencia (modificaciones en HU12)
- Uso de modelos existentes (HU18)

SPRINT 8 (21 PH):
- Auditoria (HU20)
- Exportación usa modelos existentes (HU19)

TOTAL: 8 Modelos principales + 1 Auditoría
"""