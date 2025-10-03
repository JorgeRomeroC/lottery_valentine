from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User
from apps.contest.models import Participant, Winner


class ParticipantListEndpointTests(TestCase):
    """Tests para el endpoint de lista de participantes"""

    def setUp(self):
        self.client = APIClient()

        # Crear admin
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            full_name='Admin User',
            phone='+56912345678',
            password='admin123'
        )

        # Crear usuarios de prueba
        for i in range(5):
            user = User.objects.create_user(
                email=f'user{i}@example.com',
                full_name=f'User {i}',
                phone=f'+5691234567{i}',
                password='password123'
            )
            status_choice = 'verified' if i % 2 == 0 else 'pending'
            Participant.objects.create(
                user=user,
                status=status_choice,
                verified_at=timezone.now() if status_choice == 'verified' else None
            )

    def test_list_participants_without_auth_fails(self):
        """Test: Listar participantes sin autenticación falla"""
        response = self.client.get('/api/contest/participants/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_participants_with_auth_succeeds(self):
        """Test: Listar participantes con autenticación exitoso"""
        # Login
        login_response = self.client.post('/api/users/admin/login/', {
            'email': 'admin@example.com',
            'password': 'admin123'
        }, format='json')

        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Listar participantes
        response = self.client.get('/api/contest/participants/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)


class DrawWinnerEndpointTests(TestCase):
    """Tests para el endpoint de sorteo"""

    def setUp(self):
        self.client = APIClient()

        # Crear admin
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            full_name='Admin User',
            phone='+56912345678',
            password='admin123'
        )

        # Login admin
        login_response = self.client.post('/api/users/admin/login/', {
            'email': 'admin@example.com',
            'password': 'admin123'
        }, format='json')

        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Crear participantes verificados
        for i in range(3):
            user = User.objects.create_user(
                email=f'verified{i}@example.com',
                full_name=f'Verified User {i}',
                phone=f'+5691234567{i}',
                password='password123'
            )
            user.is_verified = True
            user.save()

            Participant.objects.create(
                user=user,
                status='verified',
                verified_at=timezone.now()
            )

    def test_draw_winner_without_auth_fails(self):
        """Test: Sortear sin autenticación falla"""
        client = APIClient()  # Cliente sin token
        response = client.post('/api/contest/draw-winner/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_draw_winner_successfully(self):
        """Test: Sorteo exitoso"""
        response = self.client.post('/api/contest/draw-winner/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('winner', response.data)
        self.assertIn('message', response.data)

        # Verificar que se creó el ganador
        winner = Winner.objects.first()
        self.assertIsNotNone(winner)
        self.assertEqual(winner.participant.status, 'verified')

    def test_draw_winner_without_verified_participants_fails(self):
        """Test: Sorteo sin participantes verificados falla"""
        # Eliminar todos los participantes verificados
        Participant.objects.all().delete()

        response = self.client.post('/api/contest/draw-winner/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class LatestWinnerEndpointTests(TestCase):
    """Tests para el endpoint de último ganador"""

    def setUp(self):
        self.client = APIClient()

        # Crear admin y hacer login
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            full_name='Admin User',
            phone='+56912345678',
            password='admin123'
        )

        login_response = self.client.post('/api/users/admin/login/', {
            'email': 'admin@example.com',
            'password': 'admin123'
        }, format='json')

        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_latest_winner_when_none_exists(self):
        """Test: Obtener último ganador cuando no hay ninguno"""
        response = self.client.get('/api/contest/latest-winner/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_latest_winner_successfully(self):
        """Test: Obtener último ganador exitosamente"""
        # Crear ganador
        user = User.objects.create_user(
            email='winner@example.com',
            full_name='Winner User',
            phone='+56912345678',
            password='password123'
        )
        user.is_verified = True
        user.save()

        participant = Participant.objects.create(
            user=user,
            status='verified',
            verified_at=timezone.now()
        )
        winner = Winner.objects.create(
            participant=participant,
            is_notified=True,
            notified_at=timezone.now()
        )

        response = self.client.get('/api/contest/latest-winner/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('participant', response.data)

    class ParticipantStatsEndpointTests(TestCase):
        """Tests para el endpoint de estadísticas"""

        def setUp(self):
            self.client = APIClient()

            # Crear admin y login
            self.admin = User.objects.create_superuser(
                email='admin@example.com',
                full_name='Admin',
                phone='+56912345678',
                password='admin123'
            )

            login_response = self.client.post('/api/users/admin/login/', {
                'email': 'admin@example.com',
                'password': 'admin123'
            }, format='json')

            token = login_response.data['access']
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

            # Crear participantes
            for i in range(10):
                user = User.objects.create_user(
                    email=f'user{i}@example.com',
                    full_name=f'User {i}',
                    phone=f'+5691234567{i}',
                    password='password123'
                )
                status_val = 'verified' if i < 7 else 'pending'
                Participant.objects.create(user=user, status=status_val)

        def test_get_stats_successfully(self):
            """Test: Obtener estadísticas exitosamente"""
            response = self.client.get('/api/contest/participants/stats/')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['total_participants'], 10)
            self.assertEqual(response.data['verified_participants'], 7)
            self.assertEqual(response.data['pending_participants'], 3)