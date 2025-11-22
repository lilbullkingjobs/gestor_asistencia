import os
import sys
import django

# === Configurar el entorno Django de forma dinámica ===
# Ubicación actual: gestor_asistencia/scripts/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # Agrega la raíz del proyecto al PATH de Python

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'gestor_asistencia.settings'  # 👈 usa este nombre, no el doble "gestor_asistencia.gestor_asistencia"
)

django.setup()


from gestorApp.models import Usuario, Director, Profesor, Curso


def run():
    # ==========================
    # 1️⃣ Crear Director Alberto
    # ==========================
    director_usuario, _ = Usuario.objects.get_or_create(
        correo='alberto@colegio.cl',
        defaults={
            'nombre': 'Alberto',
            'contrasena': '1234',
            'rol': 'director',
            'estado': True,
        }
    )

    director, _ = Director.objects.get_or_create(
        usuario=director_usuario,
        defaults={'oficina': 'Dirección', 'telefono': '987654321'}
    )

    print("✅ Director creado o existente:", director.usuario.nombre)

    # ==========================
    # 2️⃣ Crear Profesor General
    # ==========================
    profesor_usuario, _ = Usuario.objects.get_or_create(
        correo='profesor@general.cl',
        defaults={
            'nombre': 'Profesor General',
            'contrasena': '1234',
            'rol': 'profesor',
            'estado': True,
        }
    )

    profesor, _ = Profesor.objects.get_or_create(
        usuario=profesor_usuario,
        defaults={'director': director, 'oficina': 'Sala 1', 'telefono': '912345678'}
    )

    print("✅ Profesor creado o existente:", profesor.usuario.nombre)

    # ==========================
    # 3️⃣ Crear todos los cursos
    # ==========================
    basicos = [f"{i}° Básico" for i in range(1, 9)]
    medios = [f"{i}° Medio" for i in range(1, 5)]
    cursos_creados = 0

    for nombre in basicos + medios:
        _, created = Curso.objects.get_or_create(nombre=nombre, profesor=profesor)
        if created:
            cursos_creados += 1

    print(f"✅ Se han creado {cursos_creados} cursos nuevos.")
    print("🎓 Datos base cargados correctamente.")


if __name__ == "__main__":
    run()
