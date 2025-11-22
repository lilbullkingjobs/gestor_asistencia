from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from gestorApp.models import Usuario

class Command(BaseCommand):
    help = 'Hashea todas las contraseñas en texto plano existentes'

    def handle(self, *args, **kwargs):
        usuarios = Usuario.objects.all()
        actualizados = 0
        
        for usuario in usuarios:
            # Verificar si la contraseña ya está hasheada
            # Las contraseñas hasheadas empiezan con 'pbkdf2_sha256$'
            if not usuario.contrasena.startswith('pbkdf2_sha256$'):
                password_original = usuario.contrasena
                usuario.contrasena = make_password(password_original)
                usuario.save()
                actualizados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Usuario {usuario.nombre} actualizado')
                )
        
        if actualizados == 0:
            self.stdout.write(
                self.style.WARNING('⚠️  No hay contraseñas por actualizar')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'🎉 Total actualizados: {actualizados}')
            )