from django.db import models


# ============================
#         USUARIO
# ============================
class Usuario(models.Model):
    ROL_CHOICES = [
        ('matrona', 'Matrona'),
        ('medico', 'Médico'),
        ('jefe_area', 'Jefe de Área'),
        ('admin', 'Administrador'),
    ]

    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)

    def __str__(self):
        return f"{self.nombre} ({self.rol})"



# ============================
#           MADRE
# ============================
class Madre(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre



# ============================
#            PARTO
# ============================
class Parto(models.Model):
    madre = models.ForeignKey(Madre, on_delete=models.CASCADE, related_name='partos')
    fecha_parto = models.DateField()  # mejor para reportes
    tipo_parto = models.CharField(max_length=50)  # normal, cesarea, inducido
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Parto de {self.madre.nombre} el {self.fecha_parto}"



# ============================
#        RECIÉN NACIDO
# ============================
class RecienNacido(models.Model):
    parto = models.OneToOneField(Parto, on_delete=models.CASCADE, related_name='rn')
    peso = models.FloatField()
    talla = models.FloatField()
    apgar = models.IntegerField()

    def __str__(self):
        return f"RN del parto {self.parto.id}"



# ============================
#        INFORME REM 22
# ============================
class InformeREM(models.Model):
    fecha = models.DateField()
    total_partos = models.IntegerField()
    total_rn = models.IntegerField()

    def __str__(self):
        return f"Informe REM {self.fecha}"
