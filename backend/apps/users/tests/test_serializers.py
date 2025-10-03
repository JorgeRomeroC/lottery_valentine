from django.test import TestCase
from apps.users.serializers import UserRegistrationSerializer, SetPasswordSerializer
from apps.users.models import User


class UserRegistrationSerializerTests(TestCase):
    """Tests para UserRegistrationSerializer"""

    def test_valid_registration_data(self):
        """Test: Datos de registro válidos"""
        data = {
            'email': 'nuevo@example.com',
            'full_name': 'María González',
            'phone': '+56987654321'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_duplicate_email_validation(self):
        """Test: Email duplicado es rechazado"""
        User.objects.create_user(
            email='existente@example.com',
            full_name='Usuario Existente',
            phone='+56912345678',
            password='password123'
        )

        data = {
            'email': 'existente@example.com',
            'full_name': 'Nuevo Usuario',
            'phone': '+56987654321'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_name_too_short_validation(self):
        """Test: Nombre muy corto es rechazado"""
        data = {
            'email': 'test@example.com',
            'full_name': 'Jo',
            'phone': '+56912345678'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('full_name', serializer.errors)

    def test_name_with_numbers_validation(self):
        """Test: Nombre con números es rechazado"""
        data = {
            'email': 'test@example.com',
            'full_name': 'Juan123',
            'phone': '+56912345678'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('full_name', serializer.errors)

    def test_invalid_phone_format_validation(self):
        """Test: Teléfono con formato inválido es rechazado"""
        invalid_phones = [
            '912345678',
            '+5691234567',
            '56912345678',
        ]

        for phone in invalid_phones:
            data = {
                'email': 'test@example.com',
                'full_name': 'Juan Pérez',
                'phone': phone
            }
            serializer = UserRegistrationSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn('phone', serializer.errors)

    def test_valid_chilean_phone_formats(self):
        """Test: Formatos de teléfono chileno válidos"""
        valid_phones = [
            '+56912345678',
            '+56987654321',
            '+56223456789',
        ]

        for phone in valid_phones:
            data = {
                'email': f'test{phone[-4:]}@example.com',
                'full_name': 'Juan Pérez',
                'phone': phone
            }
            serializer = UserRegistrationSerializer(data=data)
            self.assertTrue(serializer.is_valid())


class SetPasswordSerializerTests(TestCase):
    """Tests para SetPasswordSerializer"""

    def test_valid_password_data(self):
        """Test: Contraseñas válidas y coincidentes"""
        data = {
            'token': 'fake-token-uuid',
            'password': 'Password123!',
            'password_confirm': 'Password123!'
        }
        serializer = SetPasswordSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_passwords_must_match(self):
        """Test: Contraseñas deben coincidir"""
        data = {
            'token': 'fake-token-uuid',
            'password': 'Password123!',
            'password_confirm': 'DifferentPassword123!'
        }
        serializer = SetPasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_password_minimum_length(self):
        """Test: Contraseña debe tener mínimo 8 caracteres"""
        data = {
            'token': 'fake-token-uuid',
            'password': 'Pass12',
            'password_confirm': 'Pass12'
        }
        serializer = SetPasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())