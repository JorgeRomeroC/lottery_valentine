from django.test import TestCase
from django.utils import timezone
from apps.users.models import User
from apps.contest.models import Participant, Winner


class ParticipantModelTests(TestCase):
    """Tests para el modelo Participant"""

    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(
            email='test@example.com',
            full_name='Test User',
            phone='+56912345678',
            password='password123'
        )

    def test_create_participant_successfully(self):
        """Test: Crear participante correctamente"""
        participant = Participant.objects.create(
            user=self.user,
            status='pending'
        )

        self.assertEqual(participant.user, self.user)
        self.assertEqual(participant.status, 'pending')
        self.assertIsNotNone(participant.registered_at)
        self.assertIsNone(participant.verified_at)

    def test_participant_status_choices(self):
        """Test: Estados válidos de participante"""
        valid_statuses = ['pending', 'verified', 'rejected']

        for i, status in enumerate(valid_statuses):
            # Crear un usuario diferente para cada participante
            user = User.objects.create_user(
                email=f'user{i}@example.com',
                full_name=f'User {i}',
                phone=f'+5691234567{i}',
                password='password123'
            )
            participant = Participant.objects.create(
                user=user,
                status=status
            )
            self.assertEqual(participant.status, status)

    def test_participant_string_representation(self):
        """Test: Representación en string del participante"""
        participant = Participant.objects.create(
            user=self.user,
            status='pending'
        )
        # Verificar que el string contiene el nombre del usuario
        self.assertIn('Test User', str(participant))


class WinnerModelTests(TestCase):
    """Tests para el modelo Winner"""

    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(
            email='winner@example.com',
            full_name='Winner User',
            phone='+56912345678',
            password='password123'
        )
        self.user.is_verified = True
        self.user.save()

        self.participant = Participant.objects.create(
            user=self.user,
            status='verified',
            verified_at=timezone.now()
        )

    def test_create_winner_successfully(self):
        """Test: Crear ganador correctamente"""
        winner = Winner.objects.create(
            participant=self.participant
        )

        self.assertEqual(winner.participant, self.participant)
        self.assertFalse(winner.is_notified)
        self.assertIsNone(winner.notified_at)

    def test_winner_string_representation(self):
        """Test: Representación en string del ganador"""
        winner = Winner.objects.create(
            participant=self.participant
        )
        # Verificar que el string contiene información del ganador
        self.assertIn('Winner User', str(winner))