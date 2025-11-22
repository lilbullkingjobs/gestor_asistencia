"""
Script para poblar la base de datos con datos de prueba
Guardar como: gestorApp/commands/populate_db.py

Para ejecutar: python manage.py populate_db
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from gestorApp.models import (
    Usuario, Director, Profesor, Inspector, Apoderado, 
    Alumno, Curso, Asistencia, CertificadoMedico, Notificacion
)
from datetime import date, time, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Poblar base de datos con datos de prueba'

    def handle(self, *args, **kwargs):
        self.stdout.write('🔄 Iniciando población de base de datos...\n')
        
        # Limpiar datos existentes (opcional)
        if input("¿Desea limpiar datos existentes? (s/n): ").lower() == 's':
            self.stdout.write('🗑️  Limpiando datos...')
            Asistencia.objects.all().delete()
            Notificacion.objects.all().delete()
            CertificadoMedico.objects.all().delete()
            Alumno.objects.all().delete()
            Curso.objects.all().delete()
            Apoderado.objects.all().delete()
            Inspector.objects.all().delete()
            Profesor.objects.all().delete()
            Director.objects.all().delete()
            Usuario.objects.all().delete()
            self.stdout.write('✅ Datos limpiados\n')

        # 1. CREAR DIRECTOR
        self.stdout.write('👔 Creando Director...')
        usuario_director = Usuario.objects.create(
            nombre='Carlos Méndez',
            correo='director@colegio.cl',
            contrasena=make_password('1234'),
            rol='director',
            estado=True
        )
        director = Director.objects.create(
            usuario=usuario_director,
            oficina='Dirección Principal',
            telefono='+56912345678'
        )
        self.stdout.write(f'✅ Director creado: {director.usuario.nombre}')
        self.stdout.write(f'   📧 Email: director@colegio.cl | 🔑 Password: 1234\n')

        # 2. CREAR PROFESORES
        self.stdout.write('👨‍🏫 Creando Profesores...')
        profesores = []
        profesores_data = [
            ('María González', 'maria.gonzalez@colegio.cl', 'Sala 101'),
            ('Pedro Rodríguez', 'pedro.rodriguez@colegio.cl', 'Sala 102'),
            ('Ana Martínez', 'ana.martinez@colegio.cl', 'Sala 103'),
            ('Luis Torres', 'luis.torres@colegio.cl', 'Sala 104'),
        ]
        
        for nombre, correo, oficina in profesores_data:
            usuario = Usuario.objects.create(
                nombre=nombre,
                correo=correo,
                contrasena=make_password('1234'),
                rol='profesor',
                estado=True
            )
            profesor = Profesor.objects.create(
                usuario=usuario,
                director=director,
                oficina=oficina,
                telefono='+56987654321'
            )
            profesores.append(profesor)
            self.stdout.write(f'   ✅ {nombre}')
        
        self.stdout.write(f'✅ {len(profesores)} profesores creados')
        self.stdout.write(f'   📧 Email: [nombre]@colegio.cl | 🔑 Password: 1234\n')

        # 3. CREAR INSPECTORES
        self.stdout.write('👮 Creando Inspectores...')
        inspectores = []
        inspectores_data = [
            ('Roberto Sánchez', 'roberto.sanchez@colegio.cl', 'Mañana'),
            ('Carmen López', 'carmen.lopez@colegio.cl', 'Tarde'),
        ]
        
        for nombre, correo, turno in inspectores_data:
            usuario = Usuario.objects.create(
                nombre=nombre,
                correo=correo,
                contrasena=make_password('1234'),
                rol='inspector',
                estado=True
            )
            inspector = Inspector.objects.create(
                usuario=usuario,
                director=director,
                turno=turno
            )
            inspectores.append(inspector)
            self.stdout.write(f'   ✅ {nombre} - Turno {turno}')
        
        self.stdout.write(f'✅ {len(inspectores)} inspectores creados')
        self.stdout.write(f'   📧 Email: [nombre]@colegio.cl | 🔑 Password: 1234\n')

        # 4. CREAR CURSOS
        self.stdout.write('📚 Creando Cursos...')
        cursos = []
        cursos_nombres = ['1° Medio', '2° Medio', '3° Medio', '4° Medio']
        
        for i, nombre_curso in enumerate(cursos_nombres):
            curso = Curso.objects.create(
                nombre=nombre_curso,
                profesor=profesores[i]
            )
            cursos.append(curso)
            self.stdout.write(f'   ✅ {nombre_curso} - Profesor: {profesores[i].usuario.nombre}')
        
        self.stdout.write(f'✅ {len(cursos)} cursos creados\n')

        # 5. CREAR APODERADOS Y ALUMNOS
        self.stdout.write('👨‍👩‍👧‍👦 Creando Apoderados y Alumnos...')
        
        alumnos_data = [
            # Curso 1° Medio
            ('Juan Pérez', 'juan.perez@estudiante.cl', '12345678-9', 
             'María Pérez', 'maria.perez@apoderado.cl', 'Av. Principal 123', '+56911111111', 0),
            ('Sofía Ramírez', 'sofia.ramirez@estudiante.cl', '23456789-0',
             'Carlos Ramírez', 'carlos.ramirez@apoderado.cl', 'Calle Los Pinos 456', '+56922222222', 0),
            ('Diego Castro', 'diego.castro@estudiante.cl', '34567890-1',
             'Ana Castro', 'ana.castro@apoderado.cl', 'Pasaje Las Flores 789', '+56933333333', 0),
            ('Camila Torres', 'camila.torres@estudiante.cl', '45678901-2',
             'Jorge Torres', 'jorge.torres@apoderado.cl', 'Av. Los Álamos 321', '+56944444444', 0),
            
            # Curso 2° Medio
            ('Valentina Silva', 'valentina.silva@estudiante.cl', '56789012-3',
             'Patricia Silva', 'patricia.silva@apoderado.cl', 'Calle Central 654', '+56955555555', 1),
            ('Matías Fernández', 'matias.fernandez@estudiante.cl', '67890123-4',
             'Roberto Fernández', 'roberto.fernandez@apoderado.cl', 'Paseo La Paz 987', '+56966666666', 1),
            ('Isidora Morales', 'isidora.morales@estudiante.cl', '78901234-5',
             'Claudia Morales', 'claudia.morales@apoderado.cl', 'Calle Sol 147', '+56977777777', 1),
            ('Sebastián Vega', 'sebastian.vega@estudiante.cl', '89012345-6',
             'Fernando Vega', 'fernando.vega@apoderado.cl', 'Av. Luna 258', '+56988888888', 1),
            
            # Curso 3° Medio
            ('Benjamín Vargas', 'benjamin.vargas@estudiante.cl', '90123456-7',
             'Mónica Vargas', 'monica.vargas@apoderado.cl', 'Pasaje Estrella 369', '+56999999999', 2),
            ('Martina Rojas', 'martina.rojas@estudiante.cl', '01234567-8',
             'Daniel Rojas', 'daniel.rojas@apoderado.cl', 'Calle Cometa 741', '+56900000000', 2),
            ('Lucas Herrera', 'lucas.herrera@estudiante.cl', '11234567-9',
             'Andrea Herrera', 'andrea.herrera@apoderado.cl', 'Av. Norte 852', '+56911122233', 2),
            
            # Curso 4° Medio
            ('Emma Contreras', 'emma.contreras@estudiante.cl', '21234567-0',
             'Luis Contreras', 'luis.contreras@apoderado.cl', 'Calle Sur 963', '+56922233344', 3),
            ('Agustín Soto', 'agustin.soto@estudiante.cl', '31234567-1',
             'Carolina Soto', 'carolina.soto@apoderado.cl', 'Pasaje Este 159', '+56933344455', 3),
            ('Florencia Muñoz', 'florencia.munoz@estudiante.cl', '41234567-2',
             'Pablo Muñoz', 'pablo.munoz@apoderado.cl', 'Av. Oeste 357', '+56944455566', 3),
        ]
        
        alumnos = []
        apoderados_creados = {}
        
        for alumno_data in alumnos_data:
            (nombre_alumno, correo_alumno, rut, 
             nombre_apoderado, correo_apoderado, direccion, telefono, curso_idx) = alumno_data
            
            # Crear o recuperar apoderado
            if correo_apoderado not in apoderados_creados:
                usuario_apoderado = Usuario.objects.create(
                    nombre=nombre_apoderado,
                    correo=correo_apoderado,
                    contrasena=make_password('1234'),
                    rol='apoderado',
                    estado=True
                )
                apoderado = Apoderado.objects.create(
                    usuario=usuario_apoderado,
                    direccion=direccion,
                    telefono=telefono
                )
                apoderados_creados[correo_apoderado] = apoderado
            else:
                apoderado = apoderados_creados[correo_apoderado]
            
            # Crear alumno
            usuario_alumno = Usuario.objects.create(
                nombre=nombre_alumno,
                correo=correo_alumno,
                contrasena=make_password('1234'),
                rol='alumno',
                estado=True
            )
            alumno = Alumno.objects.create(
                usuario=usuario_alumno,
                rut=rut,
                curso=cursos[curso_idx],
                apoderado=apoderado
            )
            alumnos.append(alumno)
            self.stdout.write(f'   ✅ {nombre_alumno} - {cursos[curso_idx].nombre}')
        
        self.stdout.write(f'✅ {len(alumnos)} alumnos creados')
        self.stdout.write(f'✅ {len(apoderados_creados)} apoderados creados')
        self.stdout.write(f'   📧 Email: [nombre]@apoderado.cl | 🔑 Password: 1234\n')

        # 6. CREAR ASISTENCIAS (últimos 7 días)
        self.stdout.write('📝 Creando registros de asistencia...')
        hoy = timezone.now().date()
        
        for dias_atras in range(7):
            fecha = hoy - timedelta(days=dias_atras)
            
            # Solo días laborables
            if fecha.weekday() < 5:
                for alumno in alumnos:
                    # Simular diferentes estados
                    import random
                    estado = random.choices(
                        ['Presente', 'Ausente', 'Retirado'],
                        weights=[80, 15, 5]
                    )[0]
                    
                    Asistencia.objects.create(
                        alumno=alumno,
                        fecha=fecha,
                        estado=estado,
                        hora_ingreso=time(8, 0) if estado in ['Presente', 'Retirado'] else None,
                        hora_salida=time(15, random.randint(0, 59)) if estado == 'Retirado' else None,
                        observacion='Registro de prueba' if estado != 'Presente' else None
                    )
        
        total_asistencias = Asistencia.objects.count()
        self.stdout.write(f'✅ {total_asistencias} registros de asistencia creados\n')

        # 7. CREAR NOTIFICACIONES
        self.stdout.write('📬 Creando notificaciones...')
        
        for i, alumno in enumerate(alumnos[:5]):
            Notificacion.objects.create(
                tipo='Atraso',
                mensaje=f'{alumno.usuario.nombre} llegó tarde hoy.',
                alumno=alumno,
                inspector=inspectores[0],
                apoderado=alumno.apoderado
            )
        
        total_notificaciones = Notificacion.objects.count()
        self.stdout.write(f'✅ {total_notificaciones} notificaciones creadas\n')

        # RESUMEN FINAL
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✅ BASE DE DATOS POBLADA EXITOSAMENTE'))
        self.stdout.write('='*60)
        self.stdout.write('\n📊 RESUMEN DE DATOS CREADOS:\n')
        self.stdout.write(f'   👔 Directores: {Director.objects.count()}')
        self.stdout.write(f'   👨‍🏫 Profesores: {Profesor.objects.count()}')
        self.stdout.write(f'   👮 Inspectores: {Inspector.objects.count()}')
        self.stdout.write(f'   👨‍👩‍👧‍👦 Apoderados: {Apoderado.objects.count()}')
        self.stdout.write(f'   👦 Alumnos: {Alumno.objects.count()}')
        self.stdout.write(f'   📚 Cursos: {Curso.objects.count()}')
        self.stdout.write(f'   📝 Asistencias: {Asistencia.objects.count()}')
        self.stdout.write(f'   📬 Notificaciones: {Notificacion.objects.count()}')
        
        self.stdout.write('\n🔑 CREDENCIALES DE ACCESO:\n')
        self.stdout.write('   Director:')
        self.stdout.write('   📧 director@colegio.cl | 🔑 1234')
        self.stdout.write('\n   Inspector:')
        self.stdout.write('   📧 roberto.sanchez@colegio.cl | 🔑 1234')
        self.stdout.write('\n   Profesor:')
        self.stdout.write('   📧 maria.gonzalez@colegio.cl | 🔑 1234')
        self.stdout.write('\n   Apoderado:')
        self.stdout.write('   📧 maria.perez@apoderado.cl | 🔑 1234')
        self.stdout.write('\n' + '='*60 + '\n')