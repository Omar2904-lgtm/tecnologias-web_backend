from rest_framework import serializers
from rest_framework.authtoken.models import Token
from sistema_escolar_api.models import *
import re

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'

class AlumnoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Alumnos
        fields = '__all__'

class MaestroSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Maestros
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

    def validate_nombre(self, value):
        if not value:
            raise serializers.ValidationError("El nombre del evento es obligatorio.")
        if not re.match(r"^[a-zA-Z0-9ÁÉÍÓÚáéíóúñÑ\s]+$", value):
            raise serializers.ValidationError("El nombre del evento solo permite letras, números y espacios. No se permiten caracteres especiales.")
        return value

    def validate_lugar(self, value):
        if not value:
            raise serializers.ValidationError("El lugar es obligatorio.")
        if not re.match(r"^[a-zA-Z0-9ÁÉÍÓÚáéíóúñÑ\s.,#-]+$", value):
            raise serializers.ValidationError("El lugar solo debe admitir caracteres alfanuméricos, espacios y algunos signos como .,#-")
        return value

    def validate_descripcion(self, value):
        if not value:
             raise serializers.ValidationError("La descripción breve es obligatoria.")
        if not re.match(r"^[a-zA-Z0-9ÁÉÍÓÚáéíóúñÑ\s\.,;:!?\"'\-\(\)]*$", value):
            raise serializers.ValidationError("La descripción breve solo permite letras, números, espacios y signos de puntuación básicos.")
        return value

    def validate_cupo_maximo(self, value):
        if value is None:
             raise serializers.ValidationError("El cupo máximo es obligatorio.")
        if not isinstance(value, int) or value <= 0:
            raise serializers.ValidationError("El cupo máximo debe ser un número entero positivo.")
        if value >= 1000:
            raise serializers.ValidationError("El cupo máximo no puede ser mayor o igual a 1000 (debe tener máximo 3 dígitos).")
        return value

    def validate(self, data):
        hora_inicio = data.get('hora_inicio')
        hora_fin = data.get('hora_fin')

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise serializers.ValidationError({"hora_fin": "La hora de finalización debe ser posterior a la hora de inicio."})

        publico_objetivo = data.get('publico_objetivo')
        if not publico_objetivo or not isinstance(publico_objetivo, list) or len(publico_objetivo) == 0:
            raise serializers.ValidationError({"publico_objetivo": "Debe seleccionar al menos un público objetivo."})

        programa_educativo = data.get('programa_educativo')
        es_para_estudiantes = "Estudiantes" in publico_objetivo

        if es_para_estudiantes and not programa_educativo:
            raise serializers.ValidationError({"programa_educativo": "Se debe especificar el programa educativo si el público objetivo incluye 'Estudiantes'."})
        
        if not es_para_estudiantes and programa_educativo:
            raise serializers.ValidationError({"programa_educativo": "El programa educativo solo debe especificarse si el público objetivo es 'Estudiantes'."})

        responsable = data.get('responsable')
        if not responsable:
            raise serializers.ValidationError({"responsable": "El responsable del evento es obligatorio."})
            
        return data