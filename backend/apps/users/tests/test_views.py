from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User
from apps.contest.models import Participant


class UserRegistrationEndpointTests(TestCase):
    """Tests para el endpoint de registro"""

    def setUp(self):
        self.client = APIClient()

    def test_register_user_successfully(self):
        """Test: Registro exitoso de usuario"""
        data = {
            'email': 'nuevo@example.com',
            'full_name': 'Juan Pérez',
            'phone': '+56912345678',
            'frontend_url': 'http://localhost:5173'
        }

        response = self.client.post('/api/users/register/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['email'], 'nuevo@example.com')

        user = User.objects.get(email='nuevo@example.com')
        self.assertIsNotNone(user)
        self.assertFalse(user.is_verified)

        participant = Participant.objects.get(user=user)
        self.assertEqual(participant.status, 'pending')

    def test_register_duplicate_email_fails(self):
        """Test: Registro con email duplicado falla"""
        User.objects.create_user(
            email='existente@example.com',
            full_name='Usuario Existente',
            phone='+56912345678',
            password='password123'
        )

        data = {
            'email': 'existente@example.com',
            'full_name': 'Nuevo Usuario',
            'phone': '+56987654321',
            'frontend_url': 'http://localhost:5173'
        }

        response = self.client.post('/api/users/register/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AdminLoginEndpointTests(TestCase):
    """Tests para el endpoint de login de administrador"""

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            full_name='Admin User',
            phone='+56912345678',
            password='admin123'
        )

    def test_admin_login_successfully(self):
        """Test: Login exitoso de administrador"""
        data = {
            'email': 'admin@example.com',
            'password': 'admin123'
        }

        response = self.client.post('/api/users/admin/login/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_invalid_credentials_fails(self):
        """Test: Login con credenciales inválidas falla"""
        data = {
            'email': 'admin@example.com',
            'password': 'wrongpassword'
        }

        response = self.client.post('/api/users/admin/login/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_user_cannot_login(self):
        """Test: Usuario no-admin no puede hacer login"""
        User.objects.create_user(
            email='regular@example.com',
            full_name='Regular User',
            phone='+56912345678',
            password='password123'
        )

        data = {
            'email': 'regular@example.com',
            'password': 'password123'
        }

        response = self.client.post('/api/users/admin/login/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    class VerifyEmailEndpointTests(TestCase):
        """Tests para el endpoint de verificación de email"""

        def setUp(self):
            self.client = APIClient()
            self.user = User.objects.create_user(
                email='test@example.com',
                full_name='Test User',
                phone='+56912345678',
                password='password123'
            )

        def test_verify_email_with_valid_token(self):
            """Test: Verificación con token válido"""
            data = {'token': str(self.user.verification_token)}

            response = self.client.post('/api/users/verify-email/', data, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('message', response.data)

        def test_verify_email_with_invalid_token(self):
            """Test: Verificación con token inválido"""
            data = {'token': 'invalid-token-123'}

            response = self.client.post('/api/users/verify-email/', data, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_verify_email_without_token(self):
            """Test: Verificación sin token"""
            response = self.client.post('/api/users/verify-email/', {}, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    class SetPasswordEndpointTests(TestCase):
        """Tests para el endpoint de establecer contraseña"""

        def setUp(self):
            self.client = APIClient()
            self.user = User.objects.create_user(
                email='test@example.com',
                full_name='Test User',
                phone='+56912345678',
                password='oldpassword123'
            )

        def test_set_password_successfully(self):
            """Test: Establecer contraseña exitosamente"""
            data = {
                'token': str(self.user.verification_token),
                'password': 'NewPassword123',
                'password_confirm': 'NewPassword123'
            }

            response = self.client.post('/api/users/set-password/', data, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Verificar que el usuario fue verificado
            self.user.refresh_from_db()
            self.assertTrue(self.user.is_verified)
            self.assertTrue(self.user.check_password('NewPassword123'))

        def test_set_password_with_mismatched_passwords(self):
            """Test: Contraseñas no coinciden"""
            data = {
                'token': str(self.user.verification_token),
                'password': 'Password123',
                'password_confirm': 'DifferentPassword123'
            }

            response = self.client.post('/api/users/set-password/', data, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_set_password_without_token(self):
            """Test: Establecer contraseña sin token"""
            data = {
                'password': 'Password123',
                'password_confirm': 'Password123'
            }

            response = self.client.post('/api/users/set-password/', data, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)