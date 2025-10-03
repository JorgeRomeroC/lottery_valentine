from django.test import TestCase
from apps.users.models import User
import uuid


class UserModelTests(TestCase):
    """Tests para el modelo User"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.user_data = {
            'email': 'test@example.com',
            'full_name': 'Juan Pérez',
            'phone': '+56912345678',
            'password': 'TestPassword123'
        }

    def test_create_user_successfully(self):
        """Test: Crear usuario correctamente"""
        user = User.objects.create_user(**self.user_data)

        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.full_name, 'Juan Pérez')
        self.assertEqual(user.phone, '+56912345678')
        self.assertFalse(user.is_verified)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password('TestPassword123'))
        self.assertIsInstance(user.verification_token, uuid.UUID)

    def test_email_is_normalized_to_lowercase(self):
        """Test: Email se convierte a minúsculas"""
        user = User.objects.create_user(
            email='TEST@EXAMPLE.COM',
            full_name='Test User',
            phone='+56912345678',
            password='password123'
        )
        self.assertEqual(user.email, 'test@example.com')

    def test_email_must_be_unique(self):
        """Test: Email debe ser único"""
        User.objects.create_user(**self.user_data)

        # Intentar crear otro usuario con el mismo email
        with self.assertRaises(Exception):
            User.objects.create_user(**self.user_data)

    def test_user_string_representation(self):
        """Test: Representación en string del usuario"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'test@example.com')

    def test_create_superuser(self):
        """Test: Crear superusuario"""
        admin = User.objects.create_superuser(
            email='admin@example.com',
            full_name='Admin User',
            phone='+56912345678',
            password='admin123'
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_verified)