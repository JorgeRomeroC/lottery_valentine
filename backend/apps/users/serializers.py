from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para el registro de nuevos usuarios"""

    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone']

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value.lower()

    def validate_phone(self, value):
        # Validación básica de teléfono
        if not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("El teléfono solo debe contener números.")
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