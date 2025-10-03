from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
import re


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para el registro de nuevos usuarios"""

    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone']

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value.lower()

    def validate_full_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres")
        if len(value) > 100:
            raise serializers.ValidationError("El nombre es demasiado largo")
        if not re.match(r'^[a-záéíóúñA-ZÁÉÍÓÚÑ\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras")
        return value

    def validate_phone(self, value):
        # Validar formatos chilenos:
        # Móvil: +569XXXXXXXX (10 dígitos totales)
        # Fijo: +562XXXXXXXX (10 dígitos totales)
        if not re.match(r'^\+56[2-9]\d{8}$', value):
            raise serializers.ValidationError(
                "El teléfono debe tener formato chileno válido: +56912345678"
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class SetPasswordSerializer(serializers.Serializer):
    """Serializer para establecer la contraseña después de verificar el email"""

    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})

        # Validar la fortaleza de la contraseña
        validate_password(attrs['password'])

        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Serializer básico de usuario"""

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone', 'is_verified', 'date_joined']
        read_only_fields = ['id', 'is_verified', 'date_joined']


class AdminLoginSerializer(serializers.Serializer):
    """Serializer para login de administrador"""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})