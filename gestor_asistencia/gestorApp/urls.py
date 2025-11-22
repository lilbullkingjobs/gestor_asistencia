from django.urls import path
from . import views

urlpatterns = [
    # ============================================#
    # PÁGINA DE INICIO (Redirige al login)
    # ============================================#
    path('', views.home, name='home'),  
    
    #============================================#
    # SPRINT 1: Registro
    #============================================#
    path('registro-alumno/', views.registro_alumno, name='registro_alumno'),
    path('registro-inspector/', views.registro_inspector, name='registro_inspector'),
    
    #============================================#
    # SPRINT 2: Asistencia y Retiro
    #============================================#
    path('asistencia/', views.seleccionar_curso, name='seleccionar_curso'),
    path('asistencia/<int:curso_id>/', views.marcar_asistencia, name='marcar_asistencia'),
    path('retiro/', views.seleccionar_curso_retiro, name='seleccionar_curso_retiro'),
    path('retiro/<int:curso_id>/', views.retiro_alumno, name='retiro_alumno'),
    
    # ============================================#
    # SPRINT 3: Seguridad y Recuperación
    # ============================================#
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recuperar-contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('cambiar-contrasena/<int:usuario_id>/<str:token>/', views.cambiar_contrasena, name='cambiar_contrasena'),
    
    # ============================================#
    # SPRINT 4: Portal Apoderado y Notificaciones
    # ============================================#
    path('portal-apoderado/', views.portal_apoderado, name='portal_apoderado'),
    path('historial-asistencia/<int:alumno_id>/', views.historial_asistencia, name='historial_asistencia'),
    path('notificar-atraso/', views.notificar_atraso, name='notificar_atraso'),
    path('alerta-inasistencia/', views.alerta_inasistencia, name='alerta_inasistencia'),
    path('registrar-atraso/', views.registrar_atraso, name='registrar_atraso'),
    
    # ============================================#
    # SPRINT 5: Certificados y Monitoreo
    # ============================================#
    path('subir-certificado-medico/', views.subir_certificado_medico, name='subir_certificado_medico'),
    path('notificacion-inasistencia/', views.notificacion_inasistencia, name='notificacion_inasistencia'),
    path('monitorear-marcaje/', views.monitorear_marcaje, name='monitorear_marcaje'),
    
    # ============================================#
    # SPRINT 6: Reportes y Validaciones
    # ============================================#
    path('validar-certificados-medicos/', views.validar_certificados_medicos, name='validar_certificados_medicos'),
    path('generar-reporte-diario/', views.generar_reporte_diario, name='generar_reporte_diario'),
    path('reporte-mensual/', views.reporte_mensual, name='reporte_mensual'),
    
    # ============================================#
    # SPRINT 7: Modificación y Panel de Control
    # ============================================#
    path('modificar-asistencia-manual/', views.modificar_asistencia_manual, name='modificar_asistencia_manual'),
    path('panel-control/', views.panel_control_rol, name='panel_control_rol'),
    
    # ============================================#
    # SPRINT 8: Exportación y Auditoría
    # ============================================#
    path('exportar-reporte/', views.exportar_reporte, name='exportar_reporte'),
    path('registro-auditoria/', views.registro_auditoria, name='registro_auditoria'),
]