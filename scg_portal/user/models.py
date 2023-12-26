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
        Cuenta, on_delete=models.CASCADE, related_name="cuentas")
    
    def __str__(self):
        return self.correo
    
    def verificar_contrasena(self, raw_password):
        # Implementación para verificar la contraseña
        return raw_password == self.password