from django.contrib import admin
from .models import *

# Register your models here.
# IP   :admin
# Pass :123456

admin.site.register(Usuario)
admin.site.register(Director)
admin.site.register(Profesor)
admin.site.register(Curso)
admin.site.register(Apoderado)
admin.site.register(Alumno)
admin.site.register(Inspector)
admin.site.register(Asistencia)
admin.site.register(CertificadoMedico)
admin.site.register(Notificacion)

