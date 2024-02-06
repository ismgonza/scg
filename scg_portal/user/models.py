import random
import os
import hashlib
import time
from django.contrib.auth.hashers import check_password, make_password

from django.db import models

# Create your models here.

class Cuenta(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    correo = models.EmailField()
    password = models.CharField(max_length=150)

    TIPO_ADMIN = 'Admin'
    TIPO_CLIENTE = 'Cliente'
    OPCIONES_TIPO = [
        (TIPO_ADMIN, 'Admin'),
        (TIPO_CLIENTE, 'Cliente'),
    ]
    
    tipo = models.CharField(
        max_length=100,
        choices=OPCIONES_TIPO
    )

    cuenta = models.ForeignKey(
        Cuenta, on_delete=models.CASCADE, related_name="cuentas_usuarios")
    
    def __str__(self):
        return self.correo
    
    def verificar_contrasena(self, raw_password):
        # Implementación para verificar la contraseña
        return raw_password == self.password
    
    def set_password(self, raw_password):
        """
        Establece la contraseña del usuario cifrando la contraseña en texto plano proporcionada.
        """
        self.password = make_password(raw_password)
    
def generate_reset_token(usuario):
    # Combina el correo del usuario, la contraseña y la marca de tiempo actual para generar un token único
    token_data = f"{usuario.correo}{usuario.password}{time.time()}"
    return hashlib.sha256(token_data.encode('utf-8')).hexdigest()

def generate_nessus_filename(instance, filename):
    # No es necesario incluir la extensión aquí
    return os.path.join("nessus", f"{instance.id_reporte}_{instance.cuenta_reporte.nombre.lower()}.html")

def generate_dradis_filename(instance, filename):
    # No es necesario incluir la extensión aquí
    return os.path.join("dradis", f"{instance.id_reporte}_{instance.cuenta_reporte.nombre.lower()}.docx")
    
class Reporte(models.Model):
    id_reporte = models.IntegerField(unique=True, editable=False)
    fecha_reporte = models.DateField(auto_now=True)
    tipo_reporte = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    cuenta_reporte = models.ForeignKey(
        Cuenta, on_delete=models.CASCADE, related_name="cuentas_reportes")
    source = models.FileField(upload_to=generate_nessus_filename, null=True)
    file_report = models.FileField(upload_to=generate_dradis_filename, null=True)
    
    def __str__(self):
        return self.target
    
    def save(self, *args, **kwargs):
        # Si el objeto aún no tiene un ID asignado
        if not self.id_reporte:
            # Genera un número aleatorio único
            while True:
                nuevo_id_reporte = random.randint(100000, 999999)  # Puedes ajustar el rango según tus necesidades

                # Verifica si el número aleatorio ya existe en la base de datos
                if not Reporte.objects.filter(id_reporte=nuevo_id_reporte).exists():
                    break

            self.id_reporte = nuevo_id_reporte

        super().save(*args, **kwargs)
