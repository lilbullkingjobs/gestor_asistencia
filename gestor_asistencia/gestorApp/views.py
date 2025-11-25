from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q , Count
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Alumno, Apoderado, Curso, Usuario, Asistencia, Inspector, Director, Profesor, Notificacion, CertificadoMedico, historial_asistencia
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage
from django.db.models import Count, Q
from django.core.mail import send_mail
from datetime import date

def home(request):
    
    if request.session.get('usuario_id'):
        usuario_rol = request.session.get('usuario_rol')
        if usuario_rol == 'director':
            return redirect('panel_control_rol')
        elif usuario_rol == 'inspector':
            return redirect('panel_control_rol')  
        elif usuario_rol == 'profesor':
            return redirect('panel_control_rol')
        elif usuario_rol == 'apoderado':
            return redirect('portal_apoderado')
    
    # Si no hay sesión activa, redirigir al login
    return redirect('login')

def registro_alumno(request):
    if request.method == 'POST':
        try:
            # === Datos del alumno ===
            nombre_alumno = request.POST.get('nombre')
            correo_alumno = request.POST.get('correo')
            rut = request.POST.get('rut')
            curso_id = request.POST.get('curso')

            # === Datos del apoderado ===
            nombre_apoderado = request.POST.get('apoderado_nombre')
            correo_apoderado = request.POST.get('apoderado_correo')
            direccion_apoderado = request.POST.get('apoderado_direccion', 'No especificada')
            telefono_apoderado = request.POST.get('apoderado_telefono', 'No especificado')

            # Verificar si el apoderado ya existe
            usuario_apoderado, creado_usuario = Usuario.objects.get_or_create(
                correo=correo_apoderado,
                defaults={
                    'nombre': nombre_apoderado,
                    'contrasena': make_password('1234'),  # ✅ CAMBIO 2: Hashear contraseña
                    'rol': 'apoderado',
                    'estado': True
                }
            )

            # Crear apoderado si no existe
            apoderado, creado_apoderado = Apoderado.objects.get_or_create(
                usuario=usuario_apoderado,
                defaults={
                    'direccion': direccion_apoderado,
                    'telefono': telefono_apoderado
                }
            )

            # Crear usuario del alumno
            usuario_alumno = Usuario.objects.create(
                nombre=nombre_alumno,
                correo=correo_alumno,
                contrasena=make_password('1234'),  # ✅ CAMBIO 3: Hashear contraseña
                rol='alumno',
                estado=True
            )

            # Crear alumno asociado
            Alumno.objects.create(
                usuario=usuario_alumno,
                rut=rut,
                curso_id=curso_id,
                apoderado=apoderado
            )

            messages.success(request, "✅ Alumno y apoderado registrados correctamente.")
            return redirect('registro_alumno')

        except Exception as e:
            print("Error:", e)
            messages.error(request, f"Ocurrió un error: {e}")

    cursos = Curso.objects.all()
    return render(request, 'gestorApp/sprint_1/registro_alumno.html', {'cursos': cursos})


def registro_inspector(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            correo = request.POST.get('correo')
            turno = request.POST.get('turno')
            director_id = request.POST.get('director')
            
            # Crear usuario del inspector
            usuario = Usuario.objects.create(
                nombre=nombre,
                correo=correo,
                contrasena=make_password('1234'),  # ✅ CAMBIO 4: Hashear contraseña
                rol='inspector',
                estado=True
            )
            
            # Crear inspector
            Inspector.objects.create(
                usuario=usuario,
                director_id=director_id,
                turno=turno
            )
            
            messages.success(request, "✅ Inspector registrado correctamente.")
            return redirect('registro_inspector')
            
        except Exception as e:
            messages.error(request, f"❌ Error al registrar inspector: {e}")
    
    directores = Director.objects.all()
    return render(request, 'gestorApp/sprint_1/registro_inspector.html', {'directores': directores})


def seleccionar_curso(request):
    """Vista para seleccionar el curso antes de marcar asistencia"""
    usuario_id = request.session.get('usuario_id')
    
    if usuario_id:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            
            # Si es profesor, solo mostrar sus cursos
            if usuario.rol == 'profesor':
                profesor = Profesor.objects.get(usuario=usuario)
                cursos = Curso.objects.filter(profesor=profesor)
            else:
                # Inspectores y directores ven todos los cursos
                cursos = Curso.objects.all()
                
        except (Usuario.DoesNotExist, Profesor.DoesNotExist):
            cursos = Curso.objects.all()
    else:
        cursos = Curso.objects.all()
    
    return render(request, 'gestorApp/sprint_2/asistencia_cursos.html', {'cursos': cursos})


def marcar_asistencia(request, curso_id):
    """Vista para marcar asistencia de un curso específico con límite de tiempo"""
    from datetime import time as datetime_time
    
    curso = get_object_or_404(Curso, id=curso_id)
    alumnos = Alumno.objects.filter(curso=curso)

    fecha_hoy = timezone.now().date()
    hora_actual = timezone.now().time()
    
    # ✅ LÍMITE DE TIEMPO: 90 minutos = 1 hora 30 minutos
    # Si la clase empieza a las 08:00, se puede marcar hasta las 09:30
    HORA_INICIO_CLASES = datetime_time(8, 0)  # 08:00 AM
    HORA_LIMITE_MARCAJE = datetime_time(23, 59)  # 09:30 AM (90 minutos después)
    
    # Verificar si estamos dentro del horario permitido
    fuera_de_horario = hora_actual > HORA_LIMITE_MARCAJE
    
    # Verificar si la asistencia ya fue marcada y bloqueada
    asistencias_hoy = Asistencia.objects.filter(alumno__curso=curso, fecha=fecha_hoy)
    asistencia_bloqueada = asistencias_hoy.exists() and asistencias_hoy.first().fecha_hora_marcaje is not None
    
    # Obtener usuario actual
    usuario_id = request.session.get('usuario_id')
    usuario_actual = None
    es_inspector = False
    es_profesor = False
    
    if usuario_id:
        try:
            usuario_actual = Usuario.objects.get(id=usuario_id)
            es_inspector = usuario_actual.rol == 'inspector'
            es_profesor = usuario_actual.rol == 'profesor'
            es_director = usuario_actual.rol == 'director'
        except Usuario.DoesNotExist:
            pass

    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        # DESBLOQUEO: Solo inspectores pueden desbloquear
        if accion == 'desbloquear':
            if es_inspector:
                asistencias_hoy.update(fecha_hora_marcaje=None, marcado_por=None)
                messages.success(request, "🔓 Asistencia desbloqueada. Ahora puedes modificarla.")
                
                registrar_auditoria(
                    usuario=usuario_actual,
                    accion='Desbloqueo de Asistencia',
                    detalle=f"Desbloqueó asistencia del curso {curso.nombre} - Fecha: {fecha_hoy}",
                    tabla_afectada='Asistencia',
                    registro_id=curso.id
                )
                
                return redirect('marcar_asistencia', curso_id=curso.id)
            else:
                messages.error(request, "❌ Solo los inspectores pueden desbloquear la asistencia.")
                return redirect('marcar_asistencia', curso_id=curso.id)
        
        # BLOQUEO: Profesores e inspectores pueden bloquear (guardar asistencia)
        if accion == 'bloquear':
            if not (es_profesor or es_inspector or es_director):
                messages.error(request, "❌ No tienes permiso para marcar asistencia.")
                return redirect('marcar_asistencia', curso_id=curso.id)

            
            # ✅ VERIFICAR LÍMITE DE TIEMPO (solo para profesores)
            if es_profesor and fuera_de_horario and not asistencia_bloqueada:
                messages.error(
                    request, 
                    f"❌ El tiempo para marcar asistencia ha expirado. "
                    f"Solo se puede marcar hasta las {HORA_LIMITE_MARCAJE.strftime('%H:%M')} "
                    f"(90 minutos desde el inicio de clases). Contacta a un inspector."
                )
                return redirect('marcar_asistencia', curso_id=curso.id)
            
            # Verificar si ya está bloqueada
            if asistencia_bloqueada and es_profesor:
                messages.error(request, "❌ La asistencia ya fue marcada y bloqueada. Solo un inspector puede modificarla.")
                return redirect('marcar_asistencia', curso_id=curso.id)
            
            registros_guardados = 0
            hora_actual_marcaje = timezone.now().time()
            fecha_hora_actual = timezone.now()

            for alumno in alumnos:
                estado = request.POST.get(f"estado_{alumno.id}")
                if estado:
                    asistencia, created = Asistencia.objects.update_or_create(
                        alumno=alumno,
                        fecha=fecha_hoy,
                        defaults={
                            'estado': estado,
                            'fecha_hora_marcaje': fecha_hora_actual,
                            'marcado_por': usuario_actual,
                        }
                    )
                    
                    if estado == 'Presente' and not asistencia.hora_ingreso:
                        asistencia.hora_ingreso = hora_actual_marcaje
                    
                    if estado == 'Retirado':
                        if not asistencia.hora_salida:
                            asistencia.hora_salida = hora_actual_marcaje
                        if not asistencia.hora_ingreso:
                            asistencia.hora_ingreso = hora_actual_marcaje
                    
                    asistencia.save()
                    registros_guardados += 1

            if registros_guardados > 0:
                registrar_auditoria(
                    usuario=usuario_actual,
                    accion='Marcaje de Asistencia',
                    detalle=f"Marcó asistencia del curso {curso.nombre} - {registros_guardados} alumnos - Fecha: {fecha_hoy}",
                    tabla_afectada='Asistencia',
                    registro_id=curso.id
                )
                
                tipo_usuario = "profesor" if es_profesor else "inspector"
                messages.success(
                    request, 
                    f"✅ Asistencia registrada para {curso.nombre} a las {fecha_hora_actual.strftime('%H:%M:%S')} "
                    f"por {usuario_actual.nombre} ({tipo_usuario}). "
                    f"({registros_guardados} alumnos). La asistencia quedó bloqueada."
                )
            else:
                messages.warning(request, "⚠️ No se registraron cambios en la asistencia.")

            return redirect('marcar_asistencia', curso_id=curso.id)

    # En GET mostramos los alumnos del curso
    estado_actual = {a.alumno.id: a.estado for a in asistencias_hoy}
    
    info_marcaje = None
    if asistencias_hoy.exists():
        primera_asistencia = asistencias_hoy.first()
        if primera_asistencia.fecha_hora_marcaje:
            info_marcaje = {
                'fecha_hora': primera_asistencia.fecha_hora_marcaje,
                'marcado_por': primera_asistencia.marcado_por.nombre if primera_asistencia.marcado_por else 'Desconocido',
                'rol_marcador': primera_asistencia.marcado_por.rol if primera_asistencia.marcado_por else 'Desconocido'
            }

    # Determinar permisos del usuario actual
    puede_marcar = (es_profesor or es_inspector or es_director) and not asistencia_bloqueada and not (es_profesor and fuera_de_horario)
    puede_desbloquear = (es_inspector or es_director) and asistencia_bloqueada
    puede_ver_boton_bloquear = (es_profesor or es_inspector or es_director) and not asistencia_bloqueada and not (es_profesor and fuera_de_horario)


    return render(request, 'gestorApp/sprint_2/marcar_asistencia.html', {
        'curso': curso,
        'alumnos': alumnos,
        'estado_actual': estado_actual,
        'fecha_hoy': fecha_hoy,
        'asistencia_bloqueada': asistencia_bloqueada,
        'info_marcaje': info_marcaje,
        'puede_marcar': puede_marcar,
        'puede_desbloquear': puede_desbloquear,
        'puede_ver_boton_bloquear': puede_ver_boton_bloquear,
        'es_inspector': es_inspector,
        'es_profesor': es_profesor,
        'usuario_actual': usuario_actual,
        'fuera_de_horario': fuera_de_horario,
        'hora_limite': HORA_LIMITE_MARCAJE.strftime('%H:%M')
    })

def seleccionar_curso_retiro(request):
    """Vista para seleccionar el curso antes de retirar alumnos"""
    cursos = Curso.objects.all()
    return render(request, 'gestorApp/sprint_2/retiro_cursos.html', {'cursos': cursos})


def retiro_alumno(request, curso_id):
    """Vista para registrar el retiro de alumnos de un curso específico"""
    
    # Buscar curso o retornar 404 si no existe
    curso = get_object_or_404(Curso, id=curso_id)
    fecha_hoy = timezone.now().date()
    
    # Filtrar solo alumnos PRESENTES de este curso
    asistencias_presentes = Asistencia.objects.filter(
        fecha=fecha_hoy,
        estado='Presente',
        alumno__curso=curso
    ).select_related('alumno__usuario', 'alumno__apoderado__usuario')
    
    if request.method == 'POST':
        try:
            alumno_id = request.POST.get('alumno_id')
            apoderado_id = request.POST.get('apoderado_id')
            observacion = request.POST.get('observacion', '')
            
            # Validar que el alumno existe y está presente
            asistencia = get_object_or_404(
                Asistencia,
                alumno_id=alumno_id,
                fecha=fecha_hoy,
                estado='Presente'
            )
            
            # Actualizar asistencia a "Retirado"
            asistencia.estado = 'Retirado'
            asistencia.hora_salida = timezone.now().time()
            asistencia.observacion = observacion
            
            if apoderado_id:
                asistencia.autorizado_por_id = apoderado_id
            
            asistencia.save()
            
            messages.success(
                request, 
                f"✅ Retiro registrado: {asistencia.alumno.usuario.nombre} a las {asistencia.hora_salida.strftime('%H:%M')}"
            )
            return redirect('retiro_alumno', curso_id=curso.id)
            
        except Asistencia.DoesNotExist:
            messages.error(request, "❌ El alumno no está presente o no tiene registro de asistencia hoy.")
        except Exception as e:
            messages.error(request, f"❌ Error al registrar retiro: {e}")
    
    # Preparar datos para el template
    alumnos_presentes = []
    for asistencia in asistencias_presentes:
        alumnos_presentes.append({
            'id': asistencia.alumno.id,
            'nombre': asistencia.alumno.usuario.nombre,
            'rut': asistencia.alumno.rut,
            'hora_ingreso': asistencia.hora_ingreso,
            'apoderado': asistencia.alumno.apoderado
        })
    
    return render(request, 'gestorApp/sprint_2/retiro_alumno.html', {
        'curso': curso,
        'alumnos_presentes': alumnos_presentes,
        'fecha_hoy': fecha_hoy
    })



# ============================================
# SPRINT 3: SEGURIDAD Y RECUPERACIÓN
# ============================================

def login_view(request):
    """HU15: Inicio de sesión seguro"""
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        
        try:
            usuario = Usuario.objects.get(correo=correo)
            
            # ✅ CAMBIO 5: Verificar contraseña hasheada (CRÍTICO)
            if check_password(contrasena, usuario.contrasena):
                if usuario.estado:
                    # Guardar sesión
                    request.session['usuario_id'] = usuario.id
                    request.session['usuario_nombre'] = usuario.nombre
                    request.session['usuario_rol'] = usuario.rol
                    
                    messages.success(request, f"¡Bienvenido {usuario.nombre}!")
                    
                    # Redirigir según rol
                    if usuario.rol == 'apoderado':
                        return redirect('portal_apoderado')
                    elif usuario.rol == 'inspector':
                        return redirect('panel_control_rol')
                    elif usuario.rol == 'director':
                        return redirect('panel_control_rol')
                    else:
                        return redirect('home')
                else:
                    messages.error(request, "❌ Tu cuenta está desactivada. Contacta al administrador.")
            else:
                messages.error(request, "❌ Contraseña incorrecta.")
                
        except Usuario.DoesNotExist:
            messages.error(request, "❌ Usuario no encontrado.")
    
    return render(request, 'gestorApp/sprint_3/login.html')


def logout_view(request):
    """Cerrar sesión"""
    request.session.flush()
    messages.success(request, "✅ Sesión cerrada correctamente.")
    return redirect('login')


def recuperar_contrasena(request):
    """HU16: Recuperación de contraseña"""
    if request.method == 'POST':
        correo = request.POST.get('correo')
        
        try:
            usuario = Usuario.objects.get(correo=correo)
            
            # Generar token temporal (simulado - en producción usar tokens reales)
            token = f"temp_{usuario.id}_{timezone.now().timestamp()}"
            request.session[f'reset_token_{usuario.id}'] = token
            request.session[f'reset_email'] = correo
            
            messages.success(
                request, 
                f"✅ Se ha enviado un enlace de recuperación a {correo}. "
                "Por seguridad, el enlace expirará en 15 minutos."
            )
            
            # En producción: enviar correo con enlace
            # send_mail('Recuperación de contraseña', ...)
            
            return redirect('cambiar_contrasena', usuario_id=usuario.id, token=token)
            
        except Usuario.DoesNotExist:
            # No revelar si el correo existe (seguridad)
            messages.info(
                request, 
                "Si el correo existe, recibirás un enlace de recuperación."
            )
    
    return render(request, 'gestorApp/sprint_3/recuperar_contrasena.html')


def cambiar_contrasena(request, usuario_id, token):
    """Cambiar contraseña con token"""
    # Verificar token válido
    session_token = request.session.get(f'reset_token_{usuario_id}')
    session_email = request.session.get('reset_email')
    
    if not session_token or session_token != token:
        messages.error(request, "❌ Enlace inválido o expirado.")
        return redirect('recuperar_contrasena')
    
    if request.method == 'POST':
        nueva_contrasena = request.POST.get('nueva_contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')
        
        if nueva_contrasena != confirmar_contrasena:
            messages.error(request, "❌ Las contraseñas no coinciden.")
        elif len(nueva_contrasena) < 6:
            messages.error(request, "❌ La contraseña debe tener al menos 6 caracteres.")
        else:
            try:
                usuario = Usuario.objects.get(id=usuario_id, correo=session_email)
                usuario.contrasena = make_password(nueva_contrasena)  # ✅ CAMBIO 6: Hashear nueva contraseña
                usuario.save()
                
                # Limpiar sesión
                del request.session[f'reset_token_{usuario_id}']
                del request.session['reset_email']
                
                messages.success(request, "✅ Contraseña actualizada correctamente.")
                return redirect('login')
                
            except Usuario.DoesNotExist:
                messages.error(request, "❌ Usuario no encontrado.")
    
    return render(request, 'gestorApp/sprint_3/cambiar_contrasena.html', {
        'usuario_id': usuario_id,
        'token': token
    })


# ============================================
# SPRINT 4: PORTAL APODERADO Y NOTIFICACIONES
# ============================================

def portal_apoderado(request):
    """HU4: Portal de apoderado"""
    # Verificar sesión
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id, rol='apoderado')
        apoderado = Apoderado.objects.get(usuario=usuario)
        
        # Obtener alumnos del apoderado
        alumnos = Alumno.objects.filter(apoderado=apoderado).select_related('usuario', 'curso')
        
        # Obtener notificaciones recientes
        notificaciones = Notificacion.objects.filter(
            apoderado=apoderado
        ).order_by('-fecha_envio')[:10]
        
        return render(request, 'gestorApp/sprint_4/portal_apoderado.html', {
            'apoderado': apoderado,
            'alumnos': alumnos,
            'notificaciones': notificaciones
        })
        
    except (Usuario.DoesNotExist, Apoderado.DoesNotExist):
        messages.error(request, "❌ Apoderado no encontrado.")
        return redirect('login')


def historial_asistencia(request, alumno_id):
    """HU5: Visualizar historial de asistencia"""
    # Verificar sesión
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        alumno = get_object_or_404(Alumno, id=alumno_id)
        
        # Verificar permisos (solo apoderado del alumno o personal del colegio)
        if usuario.rol == 'apoderado':
            apoderado = Apoderado.objects.get(usuario=usuario)
            if alumno.apoderado != apoderado:
                messages.error(request, "❌ No tienes permiso para ver este alumno.")
                return redirect('portal_apoderado')
        
        # Filtros opcionales
        fecha_desde = request.GET.get('fecha_desde')
        fecha_hasta = request.GET.get('fecha_hasta')
        
        asistencias = Asistencia.objects.filter(alumno=alumno)
        
        if fecha_desde:
            asistencias = asistencias.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            asistencias = asistencias.filter(fecha__lte=fecha_hasta)
        
        asistencias = asistencias.order_by('-fecha')
        
        # Estadísticas
        total_dias = asistencias.count()
        presentes = asistencias.filter(estado='Presente').count()
        ausentes = asistencias.filter(estado='Ausente').count()
        retirados = asistencias.filter(estado='Retirado').count()
        
        porcentaje_asistencia = (presentes / total_dias * 100) if total_dias > 0 else 0
        
        return render(request, 'gestorApp/sprint_4/historial_asistencia.html', {
            'alumno': alumno,
            'asistencias': asistencias,
            'estadisticas': {
                'total_dias': total_dias,
                'presentes': presentes,
                'ausentes': ausentes,
                'retirados': retirados,
                'porcentaje_asistencia': round(porcentaje_asistencia, 1)
            }
        })
        
    except Usuario.DoesNotExist:
        messages.error(request, "❌ Usuario no encontrado.")
        return redirect('login')


def notificar_atraso(request):
    """HU17: Notificación de atraso"""
    if request.method == 'POST':
        try:
            alumno_id = request.POST.get('alumno_id')
            mensaje = request.POST.get('mensaje', '')
            
            alumno = get_object_or_404(Alumno, id=alumno_id)
            
            # Verificar si hay inspector en sesión
            usuario_id = request.session.get('usuario_id')
            inspector = None
            if usuario_id:
                try:
                    usuario = Usuario.objects.get(id=usuario_id, rol='inspector')
                    inspector = Inspector.objects.get(usuario=usuario)
                except:
                    pass
            
            # Crear notificación
            notificacion = Notificacion.objects.create(
                tipo='Atraso',
                mensaje=mensaje or f"{alumno.usuario.nombre} llegó tarde el {timezone.now().strftime('%d/%m/%Y a las %H:%M')}",
                alumno=alumno,
                inspector=inspector,
                apoderado=alumno.apoderado
            )
            
            messages.success(request, f"✅ Notificación de atraso enviada al apoderado de {alumno.usuario.nombre}")
            return JsonResponse({'success': True, 'notificacion_id': notificacion.id})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


def alerta_inasistencia(request):
    """HU14: Alerta por inasistencia prolongada"""
    # Verificar sesión (debe ser inspector o director)
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        if usuario.rol not in ['inspector', 'director']:
            messages.error(request, "❌ No tienes permiso para esta acción.")
            return redirect('login')
        
        # Definir umbral de inasistencia (por ejemplo, 3 días consecutivos)
        UMBRAL_DIAS = 3
        fecha_limite = timezone.now().date() - timedelta(days=UMBRAL_DIAS)
        
        # Buscar alumnos con inasistencia prolongada
        alumnos_problema = []
        
        for alumno in Alumno.objects.all().select_related('usuario', 'curso', 'apoderado'):
            # Obtener últimas asistencias
            ultimas_asistencias = Asistencia.objects.filter(
                alumno=alumno,
                fecha__gte=fecha_limite
            ).order_by('-fecha')[:UMBRAL_DIAS]
            
            # Verificar si todas son ausentes
            if ultimas_asistencias.count() >= UMBRAL_DIAS:
                if all(a.estado == 'Ausente' for a in ultimas_asistencias):
                    alumnos_problema.append({
                        'alumno': alumno,
                        'dias_ausente': ultimas_asistencias.count(),
                        'ultima_asistencia': ultimas_asistencias.first()
                    })
        
        # Enviar notificaciones automáticas si se solicita
        if request.method == 'POST':
            notificaciones_enviadas = 0
            for item in alumnos_problema:
                alumno = item['alumno']
                
                # Verificar si ya se envió notificación hoy
                ya_notificado = Notificacion.objects.filter(
                    alumno=alumno,
                    tipo='Inasistencia Prolongada',
                    fecha_envio__date=timezone.now().date()
                ).exists()
                
                if not ya_notificado:
                    Notificacion.objects.create(
                        tipo='Inasistencia Prolongada',
                        mensaje=f"El alumno {alumno.usuario.nombre} lleva {item['dias_ausente']} días ausente consecutivos. Por favor, justificar la inasistencia.",
                        alumno=alumno,
                        inspector=Inspector.objects.filter(usuario=usuario).first() if usuario.rol == 'inspector' else None,
                        apoderado=alumno.apoderado
                    )
                    notificaciones_enviadas += 1
            
            messages.success(request, f"✅ Se enviaron {notificaciones_enviadas} alertas de inasistencia prolongada.")
            return redirect('alerta_inasistencia')
        
        return render(request, 'gestorApp/sprint_4/alerta_inasistencia.html', {
            'alumnos_problema': alumnos_problema,
            'umbral_dias': UMBRAL_DIAS
        })
        
    except Usuario.DoesNotExist:
        messages.error(request, "❌ Usuario no encontrado.")
        return redirect('login')
    
def registrar_atraso(request):
    """Vista para registrar cuando un alumno llega tarde"""
    if request.method == 'POST':
        try:
            alumno_id = request.POST.get('alumno_id')
            observacion = request.POST.get('observacion', '')
            
            alumno = get_object_or_404(Alumno, id=alumno_id)
            fecha_hoy = timezone.now().date()
            hora_actual = timezone.now().time()
            
            # Obtener usuario que registra el atraso
            usuario_id = request.session.get('usuario_id')
            usuario_actual = None
            if usuario_id:
                usuario_actual = Usuario.objects.get(id=usuario_id)
            
            # Crear o actualizar asistencia como "Presente" pero con atraso
            asistencia, created = Asistencia.objects.update_or_create(
                alumno=alumno,
                fecha=fecha_hoy,
                defaults={
                    'estado': 'Presente',
                    'hora_ingreso': hora_actual,
                    'observacion': f"ATRASO - Llegó a las {hora_actual.strftime('%H:%M')}. {observacion}",
                    'fecha_hora_marcaje': timezone.now(),
                    'marcado_por': usuario_actual
                }
            )
            
            # Crear notificación de atraso para el apoderado
            Notificacion.objects.create(
                tipo='Atraso',
                mensaje=f"{alumno.usuario.nombre} llegó tarde el {fecha_hoy.strftime('%d/%m/%Y')} a las {hora_actual.strftime('%H:%M')}. {observacion}",
                alumno=alumno,
                inspector=Inspector.objects.filter(usuario=usuario_actual).first() if usuario_actual and usuario_actual.rol == 'inspector' else None,
                apoderado=alumno.apoderado
            )
            
            messages.success(
                request, 
                f"✅ Atraso registrado: {alumno.usuario.nombre} ingresó a las {hora_actual.strftime('%H:%M')}. "
                f"Se notificó al apoderado."
            )
            
            return JsonResponse({
                'success': True, 
                'mensaje': f"Atraso registrado correctamente",
                'hora': hora_actual.strftime('%H:%M')
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # Vista GET para mostrar formulario de atrasos
    fecha_hoy = timezone.now().date()
    
    # Obtener alumnos que NO tienen asistencia marcada hoy
    alumnos_sin_asistencia = Alumno.objects.exclude(
        asistencias__fecha=fecha_hoy
    ).select_related('usuario', 'curso', 'apoderado__usuario').order_by('curso__nombre', 'usuario__nombre')
    
    return render(request, 'gestorApp/sprint_4/registrar_atraso.html', {
        'alumnos_sin_asistencia': alumnos_sin_asistencia,
        'fecha_hoy': fecha_hoy
    })

# ============================================
# SPRINT 5: CERTIFICADOS Y MONITOREO
# ============================================


def subir_certificado_medico(request):
    """HU6: Subir certificado médico (12 PH)"""
    # Verificar sesión de apoderado
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión como apoderado.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id, rol='apoderado')
        apoderado = Apoderado.objects.get(usuario=usuario)
        
        # Obtener alumnos del apoderado
        alumnos = Alumno.objects.filter(apoderado=apoderado).select_related('usuario')
        
        if request.method == 'POST':
            alumno_id = request.POST.get('alumno_id')
            fecha_emision = request.POST.get('fecha_emision')
            motivo = request.POST.get('motivo')
            archivo = request.FILES.get('archivo_pdf')
            
            # Validaciones
            if not all([alumno_id, fecha_emision, motivo, archivo]):
                messages.error(request, "❌ Todos los campos son obligatorios.")
                return redirect('subir_certificado_medico')
            
            # Validar extensión de archivo
            if not archivo.name.endswith('.pdf'):
                messages.error(request, "❌ Solo se permiten archivos PDF.")
                return redirect('subir_certificado_medico')
            
            # Validar tamaño (máximo 5MB)
            if archivo.size > 5 * 1024 * 1024:
                messages.error(request, "❌ El archivo no debe superar 5MB.")
                return redirect('subir_certificado_medico')
            
            # Verificar que el alumno pertenece al apoderado
            alumno = get_object_or_404(Alumno, id=alumno_id, apoderado=apoderado)
            
            # Crear certificado médico
            certificado = CertificadoMedico.objects.create(
                alumno=alumno,
                apoderado=apoderado,
                fecha_emision=fecha_emision,
                motivo=motivo,
                archivo_pdf=archivo,
                validado=False
            )
            
            # Crear notificación para inspectores
            inspectores = Inspector.objects.all()
            for inspector in inspectores:
                Notificacion.objects.create(
                    tipo='Certificado Médico',
                    mensaje=f"Nuevo certificado médico subido para {alumno.usuario.nombre}. Requiere validación.",
                    alumno=alumno,
                    inspector=inspector,
                    apoderado=apoderado
                )
            
            messages.success(
                request, 
                f"✅ Certificado médico subido correctamente para {alumno.usuario.nombre}. "
                "Será validado por el inspector."
            )
            return redirect('portal_apoderado')
        
        # Obtener certificados previos
        certificados = CertificadoMedico.objects.filter(
            apoderado=apoderado
        ).select_related('alumno__usuario').order_by('-fecha_emision')[:10]
        
        return render(request, 'gestorApp/sprint_5/subir_certificado_medico.html', {
            'alumnos': alumnos,
            'certificados': certificados
        })
        
    except (Usuario.DoesNotExist, Apoderado.DoesNotExist):
        messages.error(request, "❌ Apoderado no encontrado.")
        return redirect('login')


def notificacion_inasistencia(request):
    """HU7: Notificación de inasistencia (7 PH)"""
    # Verificar sesión (inspector o director)
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        if usuario.rol not in ['inspector', 'director']:
            messages.error(request, "❌ No tienes permiso para esta acción.")
            return redirect('login')
        
        # Obtener fecha actual
        fecha_hoy = timezone.now().date()
        
        # Buscar alumnos ausentes hoy
        alumnos_ausentes = Asistencia.objects.filter(
            fecha=fecha_hoy,
            estado='Ausente'
        ).select_related('alumno__usuario', 'alumno__apoderado__usuario', 'alumno__curso')
        
        if request.method == 'POST':
            # Envío masivo de notificaciones
            alumno_ids = request.POST.getlist('alumno_ids')
            mensaje_personalizado = request.POST.get('mensaje', '')
            
            notificaciones_enviadas = 0
            
            for alumno_id in alumno_ids:
                try:
                    asistencia = Asistencia.objects.get(
                        alumno_id=alumno_id,
                        fecha=fecha_hoy,
                        estado='Ausente'
                    )
                    
                    # Verificar si ya se envió notificación hoy
                    ya_notificado = Notificacion.objects.filter(
                        alumno_id=alumno_id,
                        tipo='Inasistencia',
                        fecha_envio__date=fecha_hoy
                    ).exists()
                    
                    if not ya_notificado:
                        mensaje = mensaje_personalizado or f"Su hijo/a {asistencia.alumno.usuario.nombre} no asistió a clases hoy {fecha_hoy.strftime('%d/%m/%Y')}. Por favor, justificar la inasistencia."
                        
                        Notificacion.objects.create(
                            tipo='Inasistencia',
                            mensaje=mensaje,
                            alumno=asistencia.alumno,
                            inspector=Inspector.objects.filter(usuario=usuario).first() if usuario.rol == 'inspector' else None,
                            apoderado=asistencia.alumno.apoderado
                        )
                        notificaciones_enviadas += 1
                        
                except Asistencia.DoesNotExist:
                    continue
            
            messages.success(request, f"✅ Se enviaron {notificaciones_enviadas} notificaciones de inasistencia.")
            return redirect('notificacion_inasistencia')
        
        return render(request, 'gestorApp/sprint_5/notificacion_inasistencia.html', {
            'alumnos_ausentes': alumnos_ausentes,
            'fecha_hoy': fecha_hoy,
            'total_ausentes': alumnos_ausentes.count()
        })
        
    except Usuario.DoesNotExist:
        messages.error(request, "❌ Usuario no encontrado.")
        return redirect('login')


def monitorear_marcaje(request):
    """HU8: Monitorear marcaje de alumnos (10 PH)"""
    # Verificar sesión (inspector o director)
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        if usuario.rol not in ['inspector', 'director']:
            messages.error(request, "❌ No tienes permiso para esta acción.")
            return redirect('login')
        
        # Obtener parámetros de filtro
        curso_id = request.GET.get('curso')
        fecha_str = request.GET.get('fecha')
        
        # Fecha por defecto: hoy
        if fecha_str:
            try:
                fecha_filtro = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                fecha_filtro = timezone.now().date()
        else:
            fecha_filtro = timezone.now().date()
        
        # Obtener todos los cursos
        cursos = Curso.objects.all().select_related('profesor__usuario')
        
        # Filtrar asistencias
        asistencias_query = Asistencia.objects.filter(fecha=fecha_filtro)
        
        if curso_id:
            asistencias_query = asistencias_query.filter(alumno__curso_id=curso_id)
        
        asistencias = asistencias_query.select_related(
            'alumno__usuario',
            'alumno__curso',
            'alumno__apoderado__usuario'
        ).order_by('alumno__curso__nombre', 'alumno__usuario__nombre')
        
        # Obtener todos los alumnos (para detectar sin registro)
        todos_alumnos_query = Alumno.objects.all()
        if curso_id:
            todos_alumnos_query = todos_alumnos_query.filter(curso_id=curso_id)
        
        todos_alumnos = todos_alumnos_query.select_related('usuario', 'curso')
        
        # Detectar alumnos sin registro de asistencia
        alumnos_con_registro = set(asistencias.values_list('alumno_id', flat=True))
        alumnos_sin_registro = [
            alumno for alumno in todos_alumnos 
            if alumno.id not in alumnos_con_registro
        ]
        
        # Estadísticas generales
        estadisticas = {
            'total_alumnos': todos_alumnos.count(),
            'presentes': asistencias.filter(estado='Presente').count(),
            'ausentes': asistencias.filter(estado='Ausente').count(),
            'retirados': asistencias.filter(estado='Retirado').count(),
            'sin_registro': len(alumnos_sin_registro)
        }
        
        # Estadísticas por curso
        if curso_id:
            curso_seleccionado = get_object_or_404(Curso, id=curso_id)
        else:
            curso_seleccionado = None
        
        # Calcular porcentajes
        if estadisticas['total_alumnos'] > 0:
            estadisticas['porcentaje_asistencia'] = round(
                (estadisticas['presentes'] / estadisticas['total_alumnos']) * 100, 1
            )
        else:
            estadisticas['porcentaje_asistencia'] = 0
        
        return render(request, 'gestorApp/sprint_5/monitorear_marcaje.html', {
            'asistencias': asistencias,
            'alumnos_sin_registro': alumnos_sin_registro,
            'cursos': cursos,
            'curso_seleccionado': curso_seleccionado,
            'fecha_filtro': fecha_filtro,
            'estadisticas': estadisticas
        })
        
    except Usuario.DoesNotExist:
        messages.error(request, "❌ Usuario no encontrado.")
        return redirect('login')


# ============================================
# SPRINT 6: REPORTES Y VALIDACIONES
# ============================================

def validar_certificados_medicos(request):
    """HU9: Validar certificados médicos (11 PH)"""
    # Verificar sesión (inspector o director)
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        if usuario.rol not in ['inspector', 'director']:
            messages.error(request, "❌ No tienes permiso para esta acción.")
            return redirect('login')
        
        if request.method == 'POST':
            certificado_id = request.POST.get('certificado_id')
            accion = request.POST.get('accion')  # 'validar' o 'rechazar'
            observacion = request.POST.get('observacion', '')
            
            try:
                certificado = CertificadoMedico.objects.get(id=certificado_id)
                
                if accion == 'validar':
                    certificado.validado = True
                    certificado.save()
                    
                    # Justificar inasistencias relacionadas
                    fecha_emision = certificado.fecha_emision
                    asistencias = Asistencia.objects.filter(
                        alumno=certificado.alumno,
                        fecha=fecha_emision,
                        estado='Ausente'
                    )
                    
                    for asistencia in asistencias:
                        asistencia.observacion = f"Justificado con certificado médico: {certificado.motivo}"
                        asistencia.save()
                    
                    # Notificar al apoderado
                    Notificacion.objects.create(
                        tipo='Certificado Validado',
                        mensaje=f"El certificado médico de {certificado.alumno.usuario.nombre} ha sido validado correctamente.",
                        alumno=certificado.alumno,
                        inspector=Inspector.objects.filter(usuario=usuario).first() if usuario.rol == 'inspector' else None,
                        apoderado=certificado.apoderado
                    )
                    
                    messages.success(request, f"✅ Certificado validado correctamente para {certificado.alumno.usuario.nombre}.")
                    
                elif accion == 'rechazar':
                    certificado.delete()
                    
                    # Notificar al apoderado
                    Notificacion.objects.create(
                        tipo='Certificado Rechazado',
                        mensaje=f"El certificado médico de {certificado.alumno.usuario.nombre} ha sido rechazado. Motivo: {observacion or 'No especificado'}",
                        alumno=certificado.alumno,
                        inspector=Inspector.objects.filter(usuario=usuario).first() if usuario.rol == 'inspector' else None,
                        apoderado=certificado.apoderado
                    )
                    
                    messages.warning(request, f"⚠️ Certificado rechazado para {certificado.alumno.usuario.nombre}.")
                
                return redirect('validar_certificados_medicos')
                
            except CertificadoMedico.DoesNotExist:
                messages.error(request, "❌ Certificado no encontrado.")
        
        # Obtener certificados pendientes de validación
        certificados_pendientes = CertificadoMedico.objects.filter(
            validado=False
        ).select_related('alumno__usuario', 'apoderado__usuario', 'alumno__curso').order_by('-fecha_emision')
        
        # Obtener certificados ya validados (últimos 20)
        certificados_validados = CertificadoMedico.objects.filter(
            validado=True
        ).select_related('alumno__usuario', 'apoderado__usuario', 'alumno__curso').order_by('-fecha_emision')[:20]
        
        return render(request, 'gestorApp/sprint_6/validar_certificados_medicos.html', {
            'certificados_pendientes': certificados_pendientes,
            'certificados_validados': certificados_validados,
            'total_pendientes': certificados_pendientes.count()
        })
        
    except Usuario.DoesNotExist:
        messages.error(request, "❌ Usuario no encontrado.")
        return redirect('login')


def generar_reporte_diario(request):
    """HU10: Generar reporte diario (9 PH)"""
    # Verificar sesión (inspector o director)
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        if usuario.rol not in ['inspector', 'director']:
            messages.error(request, "❌ No tienes permiso para esta acción.")
            return redirect('login')
        
        # Obtener fecha del reporte
        fecha_str = request.GET.get('fecha')
        if fecha_str:
            try:
                fecha_reporte = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                fecha_reporte = timezone.now().date()
        else:
            fecha_reporte = timezone.now().date()
        
        # Obtener todas las asistencias del día
        asistencias = Asistencia.objects.filter(
            fecha=fecha_reporte
        ).select_related('alumno__usuario', 'alumno__curso', 'alumno__apoderado__usuario')
        
        # Estadísticas generales
        total_alumnos = Alumno.objects.count()
        estadisticas_generales = {
            'fecha': fecha_reporte,
            'total_alumnos': total_alumnos,
            'presentes': asistencias.filter(estado='Presente').count(),
            'ausentes': asistencias.filter(estado='Ausente').count(),
            'retirados': asistencias.filter(estado='Retirado').count(),
            'sin_registro': total_alumnos - asistencias.count()
        }
        
        # Calcular porcentaje de asistencia
        if total_alumnos > 0:
            estadisticas_generales['porcentaje_asistencia'] = round(
                (estadisticas_generales['presentes'] / total_alumnos) * 100, 1
            )
        else:
            estadisticas_generales['porcentaje_asistencia'] = 0
        
        # Estadísticas por curso
        cursos = Curso.objects.all().select_related('profesor__usuario')
        estadisticas_por_curso = []
        
        for curso in cursos:
            asistencias_curso = asistencias.filter(alumno__curso=curso)
            total_alumnos_curso = Alumno.objects.filter(curso=curso).count()
            presentes = asistencias_curso.filter(estado='Presente').count()
            
            porcentaje = round((presentes / total_alumnos_curso * 100), 1) if total_alumnos_curso > 0 else 0
            
            estadisticas_por_curso.append({
                'curso': curso,
                'total_alumnos': total_alumnos_curso,
                'presentes': presentes,
                'ausentes': asistencias_curso.filter(estado='Ausente').count(),
                'retirados': asistencias_curso.filter(estado='Retirado').count(),
                'porcentaje_asistencia': porcentaje
            })
        
        # Alumnos con situaciones especiales
        alumnos_retirados = asistencias.filter(estado='Retirado')
        alumnos_ausentes = asistencias.filter(estado='Ausente')
        
        # Eventos relevantes del día
        certificados_hoy = CertificadoMedico.objects.filter(
            fecha_emision=fecha_reporte
        ).select_related('alumno__usuario')
        
        notificaciones_hoy = Notificacion.objects.filter(
            fecha_envio__date=fecha_reporte
        ).select_related('alumno__usuario')
        
        return render(request, 'gestorApp/sprint_6/generar_reporte_diario.html', {
            'fecha_reporte': fecha_reporte,
            'estadisticas_generales': estadisticas_generales,
            'estadisticas_por_curso': estadisticas_por_curso,
            'alumnos_retirados': alumnos_retirados,
            'alumnos_ausentes': alumnos_ausentes,
            'certificados_hoy': certificados_hoy,
            'notificaciones_hoy': notificaciones_hoy,
            'total_notificaciones': notificaciones_hoy.count()
        })
        
    except Usuario.DoesNotExist:
        messages.error(request, "❌ Usuario no encontrado.")
        return redirect('login')


def reporte_mensual(request):
    """HU13: Reporte mensual (8 PH)"""
    # Verificar sesión (director)
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        if usuario.rol != 'director':
            messages.error(request, "❌ Solo el director puede acceder a reportes mensuales.")
            return redirect('login')
        
        # Obtener mes y año del reporte
        mes_str = request.GET.get('mes')
        anio_str = request.GET.get('anio')
        
        if mes_str and anio_str:
            try:
                mes = int(mes_str)
                anio = int(anio_str)
            except ValueError:
                mes = timezone.now().month
                anio = timezone.now().year
        else:
            mes = timezone.now().month
            anio = timezone.now().year
        
        # Calcular primer y último día del mes
        primer_dia = date(anio, mes, 1)
        if mes == 12:
            ultimo_dia = date(anio + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia = date(anio, mes + 1, 1) - timedelta(days=1)
        
        # Obtener asistencias del mes
        asistencias_mes = Asistencia.objects.filter(
            fecha__gte=primer_dia,
            fecha__lte=ultimo_dia
        ).select_related('alumno__usuario', 'alumno__curso')
        
        # Días lectivos del mes (excluyendo fines de semana)
        dias_lectivos = 0
        dia_actual = primer_dia
        while dia_actual <= ultimo_dia:
            if dia_actual.weekday() < 5:  # Lunes a Viernes
                dias_lectivos += 1
            dia_actual += timedelta(days=1)
        
        # Estadísticas generales del mes
        total_alumnos = Alumno.objects.count()
        estadisticas_generales = {
            'mes': mes,
            'anio': anio,
            'nombre_mes': [
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ][mes - 1],
            'dias_lectivos': dias_lectivos,
            'total_alumnos': total_alumnos,
            'total_presentes': asistencias_mes.filter(estado='Presente').count(),
            'total_ausentes': asistencias_mes.filter(estado='Ausente').count(),
            'total_retirados': asistencias_mes.filter(estado='Retirado').count(),
        }
        
        # Porcentaje de asistencia mensual
        if dias_lectivos > 0 and total_alumnos > 0:
            estadisticas_generales['porcentaje_asistencia'] = round(
                (estadisticas_generales['total_presentes'] / (dias_lectivos * total_alumnos)) * 100, 1
            )
        else:
            estadisticas_generales['porcentaje_asistencia'] = 0
        
        # Top 5 alumnos con más inasistencias
        alumnos_inasistencias = asistencias_mes.filter(estado='Ausente').values(
            'alumno__usuario__nombre',
            'alumno__curso__nombre',
            'alumno__apoderado__usuario__nombre'
        ).annotate(
            total_ausencias=Count('id')
        ).order_by('-total_ausencias')[:5]
        
        # Estadísticas por curso
        cursos = Curso.objects.all().select_related('profesor__usuario')
        estadisticas_por_curso = []
        
        for curso in cursos:
            asistencias_curso = asistencias_mes.filter(alumno__curso=curso)
            total_alumnos_curso = Alumno.objects.filter(curso=curso).count()
            presentes = asistencias_curso.filter(estado='Presente').count()
            
            if dias_lectivos > 0 and total_alumnos_curso > 0:
                porcentaje = round((presentes / (dias_lectivos * total_alumnos_curso) * 100), 1)
            else:
                porcentaje = 0
            
            estadisticas_por_curso.append({
                'curso': curso,
                'total_alumnos': total_alumnos_curso,
                'total_presentes': presentes,
                'total_ausentes': asistencias_curso.filter(estado='Ausente').count(),
                'total_retirados': asistencias_curso.filter(estado='Retirado').count(),
                'porcentaje_asistencia': porcentaje
            })
        
        # Certificados médicos del mes
        certificados_mes = CertificadoMedico.objects.filter(
            fecha_emision__gte=primer_dia,
            fecha_emision__lte=ultimo_dia
        ).count()
        
        # Notificaciones enviadas en el mes
        notificaciones_mes = Notificacion.objects.filter(
            fecha_envio__date__gte=primer_dia,
            fecha_envio__date__lte=ultimo_dia
        ).values('tipo').annotate(
            total=Count('id')
        ).order_by('-total')
        
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ]

        
        return render(request, 'gestorApp/sprint_6/reporte_mensual.html', {
            'estadisticas_generales': estadisticas_generales,
            'estadisticas_por_curso': estadisticas_por_curso,
            'alumnos_inasistencias': alumnos_inasistencias,
            'certificados_mes': certificados_mes,
            'notificaciones_mes': notificaciones_mes,
            'primer_dia': primer_dia,
            'ultimo_dia': ultimo_dia,
            'meses': meses
        })
        
    except Usuario.DoesNotExist:
        messages.error(request, "❌ Usuario no encontrado.")
        return redirect('login')

# ============================================
# SPRINT 7: MODIFICACIÓN Y PANEL DE CONTROL
# ============================================

def modificar_asistencia_manual(request):
    """HU12: Modificar asistencia manualmente (13 PH)"""
    # Verificar sesión (inspector o director)
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        if usuario.rol not in ['inspector', 'director']:
            messages.error(request, "❌ No tienes permiso para modificar asistencias.")
            return redirect('login')
        
        # Obtener parámetros de búsqueda
        alumno_id = request.GET.get('alumno_id')
        curso_id = request.GET.get('curso_id')
        fecha_str = request.GET.get('fecha')
        
        # Fecha por defecto: hoy
        if fecha_str:
            try:
                fecha_filtro = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                fecha_filtro = timezone.now().date()
        else:
            fecha_filtro = timezone.now().date()
        
        if request.method == 'POST':
            try:
                asistencia_id = request.POST.get('asistencia_id')
                nuevo_estado = request.POST.get('nuevo_estado')
                nueva_hora_ingreso = request.POST.get('nueva_hora_ingreso')
                nueva_hora_salida = request.POST.get('nueva_hora_salida')
                nueva_observacion = request.POST.get('nueva_observacion', '')
                motivo_modificacion = request.POST.get('motivo_modificacion', '')
                
                # Obtener asistencia
                asistencia = get_object_or_404(Asistencia, id=asistencia_id)
                
                # Guardar valores anteriores para auditoría
                estado_anterior = asistencia.estado
                hora_ingreso_anterior = asistencia.hora_ingreso
                hora_salida_anterior = asistencia.hora_salida
                observacion_anterior = asistencia.observacion
                
                # Actualizar asistencia
                if nuevo_estado:
                    asistencia.estado = nuevo_estado
                
                if nueva_hora_ingreso:
                    asistencia.hora_ingreso = nueva_hora_ingreso
                elif nuevo_estado == 'Presente' and not asistencia.hora_ingreso:
                    asistencia.hora_ingreso = timezone.now().time()
                
                if nueva_hora_salida:
                    asistencia.hora_salida = nueva_hora_salida
                elif nuevo_estado == 'Retirado' and not asistencia.hora_salida:
                    asistencia.hora_salida = timezone.now().time()
                
                if nueva_observacion:
                    asistencia.observacion = nueva_observacion
                
                asistencia.save()
                
                # Registrar auditoría
                registrar_auditoria(
                    usuario=usuario,
                    accion='Modificación de Asistencia',
                    detalle=f"Modificó asistencia de {asistencia.alumno.usuario.nombre} - "
                            f"Estado: {estado_anterior} → {asistencia.estado}. "
                            f"Motivo: {motivo_modificacion or 'No especificado'}",
                    tabla_afectada='Asistencia',
                    registro_id=asistencia.id
                )
                
                messages.success(
                    request, 
                    f"✅ Asistencia de {asistencia.alumno.usuario.nombre} modificada correctamente."
                )
                return redirect('modificar_asistencia_manual')
                
            except Exception as e:
                messages.error(request, f"❌ Error al modificar asistencia: {e}")
        
        # Obtener cursos para filtro
        cursos = Curso.objects.all().select_related('profesor__usuario')
        
        # Filtrar asistencias
        asistencias_query = Asistencia.objects.filter(fecha=fecha_filtro)
        
        if curso_id:
            asistencias_query = asistencias_query.filter(alumno__curso_id=curso_id)
        
        if alumno_id:
            asistencias_query = asistencias_query.filter(alumno_id=alumno_id)
        
        asistencias = asistencias_query.select_related(
            'alumno__usuario',
            'alumno__curso',
            'alumno__apoderado__usuario'
        ).order_by('alumno__curso__nombre', 'alumno__usuario__nombre')
        
        # Obtener alumnos para búsqueda
        alumnos_query = Alumno.objects.all()
        if curso_id:
            alumnos_query = alumnos_query.filter(curso_id=curso_id)
        alumnos = alumnos_query.select_related('usuario', 'curso')
        
        return render(request, 'gestorApp/sprint_7/modificar_asistencia_manual.html', {
            'asistencias': asistencias,
            'cursos': cursos,
            'alumnos': alumnos,
            'fecha_filtro': fecha_filtro,
            'curso_id': curso_id,
            'alumno_id': alumno_id
        })
        
    except Usuario.DoesNotExist:
        messages.error(request, "❌ Usuario no encontrado.")
        return redirect('login')


def panel_control_rol(request):
    """HU18: Panel de control por rol (12 PH)"""
    # Verificar sesión
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        fecha_hoy = timezone.now().date()
        
        # Dashboard según rol
        if usuario.rol == 'director':
            # Estadísticas generales
            total_alumnos = Alumno.objects.count()
            total_profesores = Profesor.objects.count()
            total_inspectores = Inspector.objects.count()
            total_cursos = Curso.objects.count()
            
            # Asistencia hoy
            asistencias_hoy = Asistencia.objects.filter(fecha=fecha_hoy)
            presentes_hoy = asistencias_hoy.filter(estado='Presente').count()
            ausentes_hoy = asistencias_hoy.filter(estado='Ausente').count()
            
            porcentaje_asistencia_hoy = round(
                (presentes_hoy / total_alumnos * 100) if total_alumnos > 0 else 0, 1
            )
            
            # Certificados pendientes
            certificados_pendientes = CertificadoMedico.objects.filter(validado=False).count()
            
            # Últimas notificaciones
            ultimas_notificaciones = Notificacion.objects.all().order_by('-fecha_envio')[:10]
            
            # Cursos con baja asistencia (menos del 80%)
            cursos_baja_asistencia = []
            for curso in Curso.objects.all():
                total_alumnos_curso = Alumno.objects.filter(curso=curso).count()
                presentes_curso = asistencias_hoy.filter(
                    alumno__curso=curso, 
                    estado='Presente'
                ).count()
                
                if total_alumnos_curso > 0:
                    porcentaje = (presentes_curso / total_alumnos_curso) * 100
                    if porcentaje < 80:
                        cursos_baja_asistencia.append({
                            'curso': curso,
                            'porcentaje': round(porcentaje, 1),
                            'presentes': presentes_curso,
                            'total': total_alumnos_curso
                        })
            
            return render(request, 'gestorApp/sprint_7/panel_director.html', {
                'usuario': usuario,
                'total_alumnos': total_alumnos,
                'total_profesores': total_profesores,
                'total_inspectores': total_inspectores,
                'total_cursos': total_cursos,
                'presentes_hoy': presentes_hoy,
                'ausentes_hoy': ausentes_hoy,
                'porcentaje_asistencia_hoy': porcentaje_asistencia_hoy,
                'certificados_pendientes': certificados_pendientes,
                'ultimas_notificaciones': ultimas_notificaciones,
                'cursos_baja_asistencia': cursos_baja_asistencia,
                'fecha_hoy': fecha_hoy
            })
            
        elif usuario.rol == 'inspector':
            inspector = Inspector.objects.get(usuario=usuario)
            
            # Asistencias pendientes de marcar
            total_alumnos = Alumno.objects.count()
            asistencias_marcadas_hoy = Asistencia.objects.filter(fecha=fecha_hoy).count()
            pendientes_marcar = total_alumnos - asistencias_marcadas_hoy
            
            # Alumnos presentes que pueden ser retirados
            alumnos_presentes = Asistencia.objects.filter(
                fecha=fecha_hoy,
                estado='Presente'
            ).count()
            
            # Certificados pendientes de validación
            certificados_pendientes = CertificadoMedico.objects.filter(validado=False).count()
            
            # Notificaciones enviadas hoy
            notificaciones_hoy = Notificacion.objects.filter(
                inspector=inspector,
                fecha_envio__date=fecha_hoy
            ).count()
            
            # Últimas actividades
            ultimas_actividades = Notificacion.objects.filter(
                inspector=inspector
            ).order_by('-fecha_envio')[:10]
            
            # Tareas pendientes
            tareas_pendientes = {
                'asistencias_por_marcar': pendientes_marcar,
                'certificados_por_validar': certificados_pendientes,
                'alumnos_para_retiro': alumnos_presentes
            }
            
            return render(request, 'gestorApp/sprint_7/panel_inspector.html', {
                'usuario': usuario,
                'inspector': inspector,
                'tareas_pendientes': tareas_pendientes,
                'notificaciones_hoy': notificaciones_hoy,
                'ultimas_actividades': ultimas_actividades,
                'fecha_hoy': fecha_hoy
            })
            
        elif usuario.rol == 'profesor':
            profesor = Profesor.objects.get(usuario=usuario)
            
            # Obtener cursos del profesor
            cursos = Curso.objects.filter(profesor=profesor)
            
            # Estadísticas por curso
            estadisticas_cursos = []
            for curso in cursos:
                total_alumnos_curso = Alumno.objects.filter(curso=curso).count()
                asistencias_curso_hoy = Asistencia.objects.filter(
                    alumno__curso=curso,
                    fecha=fecha_hoy
                )
                presentes = asistencias_curso_hoy.filter(estado='Presente').count()
                ausentes = asistencias_curso_hoy.filter(estado='Ausente').count()
                
                porcentaje = round(
                    (presentes / total_alumnos_curso * 100) if total_alumnos_curso > 0 else 0, 1
                )
                
                estadisticas_cursos.append({
                    'curso': curso,
                    'total_alumnos': total_alumnos_curso,
                    'presentes': presentes,
                    'ausentes': ausentes,
                    'porcentaje': porcentaje
                })
            
            return render(request, 'gestorApp/sprint_7/panel_profesor.html', {
                'usuario': usuario,
                'profesor': profesor,
                'estadisticas_cursos': estadisticas_cursos,
                'fecha_hoy': fecha_hoy
            })
            
        elif usuario.rol == 'apoderado':
            return redirect('portal_apoderado')
            
        else:
            messages.error(request, "❌ Rol no reconocido.")
            return redirect('login')
            
    except Usuario.DoesNotExist:
        messages.error(request, "❌ Usuario no encontrado.")
        return redirect('login')
    except Exception as e:
        messages.error(request, f"❌ Error: {e}")
        return redirect('login')


# ============================================
# SPRINT 8: EXPORTACIÓN Y AUDITORÍA
# ============================================

def exportar_reporte(request):
    """HU19: Exportar reporte en PDF/Excel (8 PH)"""
    from django.http import HttpResponse
    import csv
    
    # Verificar sesión
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        if usuario.rol not in ['inspector', 'director', 'profesor']:
            messages.error(request, "❌ No tienes permiso para exportar reportes.")
            return redirect('login')
        
        # Obtener parámetros
        tipo_reporte = request.GET.get('tipo', 'diario')
        formato = request.GET.get('formato', 'csv')
        fecha_str = request.GET.get('fecha')
        curso_id = request.GET.get('curso_id')
        
        if fecha_str:
            try:
                fecha_reporte = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                fecha_reporte = timezone.now().date()
        else:
            fecha_reporte = timezone.now().date()
        
        # Registrar auditoría
        registrar_auditoria(
            usuario=usuario,
            accion='Exportación de Reporte',
            detalle=f"Exportó reporte {tipo_reporte} en formato {formato.upper()} - Fecha: {fecha_reporte}",
            tabla_afectada='Asistencia',
            registro_id=None
        )
        
        if tipo_reporte == 'diario':
            # Exportar reporte diario
            asistencias = Asistencia.objects.filter(fecha=fecha_reporte)
            
            if curso_id:
                asistencias = asistencias.filter(alumno__curso_id=curso_id)
            
            asistencias = asistencias.select_related(
                'alumno__usuario',
                'alumno__curso',
                'alumno__apoderado__usuario'
            ).order_by('alumno__curso__nombre', 'alumno__usuario__nombre')
            
            if formato == 'csv':
                response = HttpResponse(content_type='text/csv; charset=utf-8')
                response['Content-Disposition'] = f'attachment; filename="reporte_asistencia_{fecha_reporte}.csv"'
                
                # BOM para Excel
                response.write('\ufeff')
                
                writer = csv.writer(response)
                writer.writerow([
                    'Fecha', 'Curso', 'RUT', 'Alumno', 'Estado', 
                    'Hora Ingreso', 'Hora Salida', 'Apoderado', 'Observación'
                ])
                
                for asistencia in asistencias:
                    writer.writerow([
                        asistencia.fecha.strftime('%d/%m/%Y'),
                        asistencia.alumno.curso.nombre,
                        asistencia.alumno.rut,
                        asistencia.alumno.usuario.nombre,
                        asistencia.estado,
                        asistencia.hora_ingreso.strftime('%H:%M') if asistencia.hora_ingreso else '-',
                        asistencia.hora_salida.strftime('%H:%M') if asistencia.hora_salida else '-',
                        asistencia.alumno.apoderado.usuario.nombre if asistencia.alumno.apoderado else '-',
                        asistencia.observacion or '-'
                    ])
                
                return response
        
        elif tipo_reporte == 'mensual':
            # Exportar reporte mensual
            mes = fecha_reporte.month
            anio = fecha_reporte.year
            
            primer_dia = date(anio, mes, 1)
            if mes == 12:
                ultimo_dia = date(anio + 1, 1, 1) - timedelta(days=1)
            else:
                ultimo_dia = date(anio, mes + 1, 1) - timedelta(days=1)
            
            asistencias = Asistencia.objects.filter(
                fecha__gte=primer_dia,
                fecha__lte=ultimo_dia
            )
            
            if curso_id:
                asistencias = asistencias.filter(alumno__curso_id=curso_id)
            
            if formato == 'csv':
                response = HttpResponse(content_type='text/csv; charset=utf-8')
                response['Content-Disposition'] = f'attachment; filename="reporte_mensual_{mes}_{anio}.csv"'
                
                response.write('\ufeff')
                
                writer = csv.writer(response)
                writer.writerow([
                    'RUT', 'Alumno', 'Curso', 'Total Días', 'Presentes', 
                    'Ausentes', 'Retirados', '% Asistencia'
                ])
                
                # Agrupar por alumno
                alumnos = Alumno.objects.all()
                if curso_id:
                    alumnos = alumnos.filter(curso_id=curso_id)
                
                for alumno in alumnos:
                    asistencias_alumno = asistencias.filter(alumno=alumno)
                    total = asistencias_alumno.count()
                    presentes = asistencias_alumno.filter(estado='Presente').count()
                    ausentes = asistencias_alumno.filter(estado='Ausente').count()
                    retirados = asistencias_alumno.filter(estado='Retirado').count()
                    
                    porcentaje = round((presentes / total * 100) if total > 0 else 0, 1)
                    
                    writer.writerow([
                        alumno.rut,
                        alumno.usuario.nombre,
                        alumno.curso.nombre,
                        total,
                        presentes,
                        ausentes,
                        retirados,
                        f"{porcentaje}%"
                    ])
                
                return response
        
        messages.error(request, "❌ Tipo de reporte o formato no válido.")
        return redirect('panel_control_rol')
        
    except Usuario.DoesNotExist:
        messages.error(request, "❌ Usuario no encontrado.")
        return redirect('login')


def registrar_auditoria(usuario, accion, detalle, tabla_afectada, registro_id):
    """Función auxiliar para registrar auditoría"""
    from .models import Auditoria
    
    Auditoria.objects.create(
        usuario=usuario,
        accion=accion,
        detalle=detalle,
        tabla_afectada=tabla_afectada,
        registro_id=registro_id,
        fecha_hora=timezone.now()
    )


def registro_auditoria(request):
    """HU20: Registro de auditoría (13 PH)"""
    # Verificar sesión (solo director)
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        if usuario.rol != 'director':
            messages.error(request, "❌ Solo el director puede acceder al registro de auditoría.")
            return redirect('login')
        
        # Filtros
        fecha_desde = request.GET.get('fecha_desde')
        fecha_hasta = request.GET.get('fecha_hasta')
        usuario_filtro = request.GET.get('usuario_id')
        accion_filtro = request.GET.get('accion')
        tabla_filtro = request.GET.get('tabla')
        
        from .models import Auditoria
        
        auditorias = Auditoria.objects.all().select_related('usuario')
        
        if fecha_desde:
            auditorias = auditorias.filter(fecha_hora__date__gte=fecha_desde)
        
        if fecha_hasta:
            auditorias = auditorias.filter(fecha_hora__date__lte=fecha_hasta)
        
        if usuario_filtro:
            auditorias = auditorias.filter(usuario_id=usuario_filtro)
        
        if accion_filtro:
            auditorias = auditorias.filter(accion__icontains=accion_filtro)
        
        if tabla_filtro:
            auditorias = auditorias.filter(tabla_afectada=tabla_filtro)
        
        auditorias = auditorias.order_by('-fecha_hora')[:100]
        
        # Obtener listas para filtros
        usuarios_sistema = Usuario.objects.filter(
            rol__in=['inspector', 'director', 'profesor']
        ).order_by('nombre')
        
        acciones_disponibles = Auditoria.objects.values_list(
            'accion', flat=True
        ).distinct().order_by('accion')
        
        tablas_disponibles = Auditoria.objects.values_list(
            'tabla_afectada', flat=True
        ).distinct().order_by('tabla_afectada')
        
        # Estadísticas
        total_registros = auditorias.count()
        acciones_hoy = Auditoria.objects.filter(
            fecha_hora__date=timezone.now().date()
        ).count()
        
        return render(request, 'gestorApp/sprint_8/registro_auditoria.html', {
            'auditorias': auditorias,
            'usuarios_sistema': usuarios_sistema,
            'acciones_disponibles': acciones_disponibles,
            'tablas_disponibles': tablas_disponibles,
            'total_registros': total_registros,
            'acciones_hoy': acciones_hoy,
            'filtros': {
                'fecha_desde': fecha_desde,
                'fecha_hasta': fecha_hasta,
                'usuario_id': usuario_filtro,
                'accion': accion_filtro,
                'tabla': tabla_filtro
            }
        })
        
    except Usuario.DoesNotExist:
        messages.error(request, "❌ Usuario no encontrado.")
        return redirect('login')
    

def ver_certificado_medico(request):
    return render(request, 'gestorApp/sprint_5/cert_archivo_pdf.html')

def historial_asistencia(request, alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    asistencias = Asistencia.objects.filter(alumno=alumno)
    return render(request, 'sprint_4/historial_asistencia.html', {
        'alumno': alumno,
        'asistencias': asistencias
    })

def gestion_completa_director(request):
    """Vista principal de gestión del director con modales"""
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "❌ Debes iniciar sesión.")
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        if usuario.rol != 'director':
            messages.error(request, "❌ Solo el director puede acceder a esta sección.")
            return redirect('login')
        
        # Obtener todos los datos necesarios
        inspectores = Inspector.objects.all().select_related('usuario')
        apoderados = Apoderado.objects.all().select_related('usuario')
        alumnos = Alumno.objects.all().select_related('usuario', 'curso', 'apoderado__usuario')
        cursos = Curso.objects.all()
        directores = Director.objects.all()
        
        return render(request, 'gestorApp/sprint_7/gestion_director.html', {
            'usuario': usuario,
            'inspectores': inspectores,
            'apoderados': apoderados,
            'alumnos': alumnos,
            'cursos': cursos,
            'directores': directores
        })
        
    except Usuario.DoesNotExist:
        messages.error(request, "❌ Usuario no encontrado.")
        return redirect('login')


def crear_inspector(request):
    """Crear inspector desde modal"""
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "❌ Debes iniciar sesión.")
            return redirect('login')
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            if usuario.rol != 'director':
                messages.error(request, "❌ Solo el director puede crear inspectores.")
                return redirect('gestion_completa_director')
            
            nombre = request.POST.get('nombre')
            correo = request.POST.get('correo')
            turno = request.POST.get('turno')
            
            # Obtener el director actual
            director = Director.objects.get(usuario=usuario)
            
            # Crear usuario del inspector
            usuario_inspector = Usuario.objects.create(
                nombre=nombre,
                correo=correo,
                contrasena=make_password('1234'),
                rol='inspector',
                estado=True
            )
            
            # Crear inspector
            Inspector.objects.create(
                usuario=usuario_inspector,
                director=director,
                turno=turno
            )
            
            messages.success(request, f"✅ Inspector {nombre} creado correctamente.")
            
        except Exception as e:
            messages.error(request, f"❌ Error al crear inspector: {e}")
    
    return redirect('gestion_completa_director')


def editar_inspector(request, inspector_id):
    """Editar inspector desde modal"""
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "❌ Debes iniciar sesión.")
            return redirect('login')
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            if usuario.rol != 'director':
                messages.error(request, "❌ Solo el director puede editar inspectores.")
                return redirect('gestion_completa_director')
            
            inspector = get_object_or_404(Inspector, id=inspector_id)
            
            # Actualizar datos
            inspector.usuario.nombre = request.POST.get('nombre')
            inspector.usuario.correo = request.POST.get('correo')
            inspector.turno = request.POST.get('turno')
            
            estado = request.POST.get('estado')
            inspector.usuario.estado = (estado == 'activo')
            
            inspector.usuario.save()
            inspector.save()
            
            messages.success(request, f"✅ Inspector {inspector.usuario.nombre} actualizado correctamente.")
            
        except Exception as e:
            messages.error(request, f"❌ Error al editar inspector: {e}")
    
    return redirect('gestion_completa_director')


def eliminar_inspector(request, inspector_id):
    """Desactivar inspector"""
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "❌ Debes iniciar sesión.")
            return redirect('login')
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            if usuario.rol != 'director':
                messages.error(request, "❌ Solo el director puede desactivar inspectores.")
                return redirect('gestion_completa_director')
            
            inspector = get_object_or_404(Inspector, id=inspector_id)
            inspector.usuario.estado = False
            inspector.usuario.save()
            
            messages.success(request, f"✅ Inspector {inspector.usuario.nombre} desactivado correctamente.")
            
        except Exception as e:
            messages.error(request, f"❌ Error al desactivar inspector: {e}")
    
    return redirect('gestion_completa_director')


def crear_apoderado_con_alumno(request):
    """Crear apoderado y alumno desde modal"""
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "❌ Debes iniciar sesión.")
            return redirect('login')
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            if usuario.rol != 'director':
                messages.error(request, "❌ Solo el director puede crear apoderados.")
                return redirect('gestion_completa_director')
            
            # Datos del apoderado
            apoderado_nombre = request.POST.get('apoderado_nombre')
            apoderado_correo = request.POST.get('apoderado_correo')
            apoderado_telefono = request.POST.get('apoderado_telefono', 'No especificado')
            apoderado_direccion = request.POST.get('apoderado_direccion', 'No especificada')
            
            # Datos del alumno
            alumno_nombre = request.POST.get('alumno_nombre')
            alumno_correo = request.POST.get('alumno_correo')
            alumno_rut = request.POST.get('alumno_rut')
            curso_id = request.POST.get('curso_id')
            
            # Crear o obtener apoderado
            usuario_apoderado, created = Usuario.objects.get_or_create(
                correo=apoderado_correo,
                defaults={
                    'nombre': apoderado_nombre,
                    'contrasena': make_password('1234'),
                    'rol': 'apoderado',
                    'estado': True
                }
            )
            
            apoderado, created_apo = Apoderado.objects.get_or_create(
                usuario=usuario_apoderado,
                defaults={
                    'telefono': apoderado_telefono,
                    'direccion': apoderado_direccion
                }
            )
            
            # Crear alumno
            usuario_alumno = Usuario.objects.create(
                nombre=alumno_nombre,
                correo=alumno_correo,
                contrasena=make_password('1234'),
                rol='alumno',
                estado=True
            )
            
            Alumno.objects.create(
                usuario=usuario_alumno,
                rut=alumno_rut,
                curso_id=curso_id,
                apoderado=apoderado
            )
            
            messages.success(request, f"✅ Apoderado {apoderado_nombre} y alumno {alumno_nombre} creados correctamente.")
            
        except Exception as e:
            messages.error(request, f"❌ Error al crear apoderado y alumno: {e}")
    
    return redirect('gestion_completa_director')


def editar_apoderado(request, apoderado_id):
    """Editar apoderado desde modal"""
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "❌ Debes iniciar sesión.")
            return redirect('login')
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            if usuario.rol != 'director':
                messages.error(request, "❌ Solo el director puede editar apoderados.")
                return redirect('gestion_completa_director')
            
            apoderado = get_object_or_404(Apoderado, id=apoderado_id)
            
            # Actualizar datos
            apoderado.usuario.nombre = request.POST.get('nombre')
            apoderado.usuario.correo = request.POST.get('correo')
            apoderado.telefono = request.POST.get('telefono', 'No especificado')
            apoderado.direccion = request.POST.get('direccion', 'No especificada')
            
            estado = request.POST.get('estado')
            apoderado.usuario.estado = (estado == 'activo')
            
            apoderado.usuario.save()
            apoderado.save()
            
            messages.success(request, f"✅ Apoderado {apoderado.usuario.nombre} actualizado correctamente.")
            
        except Exception as e:
            messages.error(request, f"❌ Error al editar apoderado: {e}")
    
    return redirect('gestion_completa_director')


def eliminar_apoderado(request, apoderado_id):
    """Desactivar apoderado"""
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "❌ Debes iniciar sesión.")
            return redirect('login')
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            if usuario.rol != 'director':
                messages.error(request, "❌ Solo el director puede desactivar apoderados.")
                return redirect('gestion_completa_director')
            
            apoderado = get_object_or_404(Apoderado, id=apoderado_id)
            apoderado.usuario.estado = False
            apoderado.usuario.save()
            
            messages.success(request, f"✅ Apoderado {apoderado.usuario.nombre} desactivado correctamente.")
            
        except Exception as e:
            messages.error(request, f"❌ Error al desactivar apoderado: {e}")
    
    return redirect('gestion_completa_director')

# ============================================
# MODIFICACION DE ASISTENCIA MANUAL
# ============================================

