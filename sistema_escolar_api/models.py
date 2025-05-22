from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings



class BearerTokenAuthentication(TokenAuthentication):
    keyword = u"Bearer"

    

class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    clave_admin = models.CharField(max_length=255,null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    ocupacion = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del admin "+self.first_name+" "+self.last_name
    
#ALUMNOS

class Alumnos(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    matricula = models.IntegerField(null=True, blank=True)
    fecha_nacimiento = models.CharField(max_length=255,null=True, blank=True)
    curp = models.CharField(max_length=255,null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    ocupacion = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del alumno "+self.first_name+" "+self.last_name
    
class Maestros(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    id_trabajador = models.IntegerField(null=True, blank=True)
    fecha_nacimiento = models.CharField(max_length=255,null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    cubiculo = models.CharField(max_length=255,null=True, blank=True)
    area_investigacion = models.CharField(max_length=255,null=True, blank=True)
    materias_json = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)


class Evento(models.Model):
    TIPO_EVENTO_CHOICES = [ # [cite: 11]
        ('Conferencia', 'Conferencia'), # [cite: 12]
        ('Taller', 'Taller'), # [cite: 12]
        ('Seminario', 'Seminario'), # [cite: 12]
        ('Concurso', 'Concurso'), # [cite: 12]
    ]

    # Opciones para el campo 'programa_educativo'
    PROGRAMA_EDUCATIVO_CHOICES = [ # [cite: 7]
        ('ICC', 'Ingeniería en Ciencias de la Computación'), # [cite: 7]
        ('LCC', 'Licenciatura en Ciencias de la Computación'), # [cite: 7]
        ('ITI', 'Ingeniería en Tecnologías de la Información'), # [cite: 7]
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPO_EVENTO_CHOICES)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    lugar = models.CharField(max_length=100)

    publico_objetivo = models.JSONField(default=list) # default=list es una buena práctica

    programa_educativo = models.CharField(
        max_length=100, # O considera un max_length más corto si guardas claves como 'ICC'
        choices=PROGRAMA_EDUCATIVO_CHOICES,
        blank=True,
        null=True
    )

    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL, # o 'User' si lo importaste directamente
        on_delete=models.SET_NULL,
        null=True
    )

    descripcion = models.TextField(max_length=300) # Límite máximo de 300 caracteres. [cite: 20]
    cupo_maximo = models.PositiveIntegerField() # Solo números enteros positivos. [cite: 22] El límite de 3 dígitos se valida en el form/serializer. [cite: 22]

    def __str__(self):
        return "Perfil del maestro "+self.first_name+" "+self.last_name
    

class Meta:
        verbose_name = "Evento Académico"
        verbose_name_plural = "Eventos Académicos"