import random
import os
import hashlib
import time
from django.contrib.auth.hashers import make_password
from django.conf import settings

from django.db import models

# Create your models here.

class Cuenta(models.Model):
    id_cuenta = models.IntegerField(unique=True, editable=False)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Si el objeto aún no tiene un ID asignado
        if not self.id_cuenta:
            # Genera un número aleatorio único
            while True:
                nuevo_id_cuenta = random.randint(100000, 999999)  # Puedes ajustar el rango según tus necesidades

                # Verifica si el número aleatorio ya existe en la base de datos
                if not Cuenta.objects.filter(id_cuenta=nuevo_id_cuenta).exists():
                    break

            self.id_cuenta = nuevo_id_cuenta

        super().save(*args, **kwargs)

class Usuario(models.Model):
    user_id = models.BigAutoField(primary_key=True)
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
    
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)

    STATUS_EN = 'Enabled'
    STATUS_DIS = 'Disabled'
    OPCIONES_STATUS = [
        (STATUS_EN, 'Enabled'),
        (STATUS_DIS, 'Disabled')
    ]

    status = models.CharField(
        max_length=100,
        choices=OPCIONES_STATUS
    )
    
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
    # Genera el nombre de archivo para uploads
    upload_file = os.path.join("nessus", f"{instance.id_reporte}_{instance.cuenta_reporte.nombre.lower()}.json")
    # Guarda una copia del archivo en static/reports
    static_reports_path = os.path.join(settings.BASE_DIR, "static", "reports")
    static_file = os.path.join(static_reports_path, f"{instance.id_reporte}.json")
    return upload_file  # Solo devuelve la ruta de archivo para uploads

def generate_dradis_filename(instance, filename):
    # No es necesario incluir la extensión aquí
    return os.path.join("dradis", f"{instance.id_reporte}_{instance.cuenta_reporte.nombre.lower()}.docx")
    
class Reporte(models.Model):
    id_reporte = models.IntegerField(unique=True, editable=False)
    fecha_reporte = models.DateField(auto_now_add=True)
    tipo_reporte = models.CharField(max_length=100)
    target = models.CharField(max_length=100, null=True)
    cuenta_reporte = models.ForeignKey(
        Cuenta, on_delete=models.CASCADE, related_name="cuentas_reportes")
    source = models.FileField(upload_to=generate_nessus_filename, null=True, blank=True)
    file_report = models.FileField(upload_to=generate_dradis_filename, null=True, blank=True)
    
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

        # Copiar el archivo JSON a static/reports
        static_reports_path = os.path.join(settings.BASE_DIR, "static", "reports")
        os.makedirs(static_reports_path, exist_ok=True)  # Crea la carpeta si no existe
        static_file = os.path.join(static_reports_path, f"{self.id_reporte}.json")
        with open(static_file, "wb") as destination_file:
            with self.source.open("rb") as source_file:
                destination_file.write(source_file.read())

class Tarea(models.Model):
    id_tarea = models.IntegerField(unique=True, editable=False)
    cuenta_tarea = models.ForeignKey(
        Cuenta, on_delete=models.CASCADE, related_name="cuentas_tareas")
    
    SEV_1 = '1'
    SEV_2 = '2'
    SEV_3 = '3'
    OPCIONES_SEV = [
        (SEV_1, '1'),
        (SEV_2, '2'),
        (SEV_3, '3')
    ]

    severity = models.CharField(max_length=100, choices=OPCIONES_SEV)
    fecha = models.DateField(auto_now_add=True)
    fecha_final = models.DateField(null=True, blank=True)
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    incidente = models.CharField(max_length=100)
    asignee = models.CharField(max_length=100, null=True, blank=True)

    STATUS_COMP = 'Completed'
    STATUS_INP = 'In Progress'
    STATUS_PEND = 'Pending'
    STATUS_NST = 'Not Started'
    OPCIONES_STATUS = [
        (STATUS_COMP, 'Completed'),
        (STATUS_INP, 'In Progress'),
        (STATUS_PEND, 'Pending'),
        (STATUS_NST, 'Not Started')
    ]

    status = models.CharField(
        max_length=100,
        choices=OPCIONES_STATUS
    )

    loe = models.FloatField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.incidente
    
    def save(self, *args, **kwargs):
        # Si el objeto aún no tiene un ID asignado
        if not self.id_tarea:
            # Genera un número aleatorio único
            while True:
                nuevo_id_tarea = random.randint(100000, 999999)  # Puedes ajustar el rango según tus necesidades

                # Verifica si el número aleatorio ya existe en la base de datos
                if not Tarea.objects.filter(id_tarea=nuevo_id_tarea).exists():
                    break

            self.id_tarea = nuevo_id_tarea

        super().save(*args, **kwargs)

class Contrato(models.Model):
    id_contrato = models.IntegerField()
    cuenta_contrato = models.ForeignKey(
        Cuenta, on_delete=models.CASCADE, related_name="cuentas_contratos")
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()

    STATUS_ACT = 'Active'
    STATUS_INACT = 'Inactive'
    OPCIONES_STATUS = [
        (STATUS_ACT, 'Active'),
        (STATUS_INACT, 'Inactive')
    ]

    status = models.CharField(
        max_length=100,
        choices=OPCIONES_STATUS
    )

    def __str__(self):
        return self.status
    
class Comment(models.Model):
    id_comment = models.BigAutoField(primary_key=True)
    tarea_comment = models.ForeignKey(
        Tarea, on_delete=models.CASCADE, related_name="tareas_comments")
    nombre = models.CharField(max_length=100, null=True)
    comment = models.TextField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    loe = models.FloatField(max_length=100, null=True, blank=True)