from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch
from apps.contest.tasks import send_participation_confirmation_email, send_winner_notification_email


class SendParticipationConfirmationEmailTests(TestCase):
    """Tests para email de confirmación de participación"""

    @patch('apps.contest.tasks.send_mail')
    def test_send_participation_confirmation_successfully(self, mock_send_mail):
        """Test: Envío exitoso de confirmación de participación"""
        mock_send_mail.return_value = 1

        result = send_participation_confirmation_email(
            user_email='participant@example.com',
            user_name='Participant User'
        )

        mock_send_mail.assert_called_once()

        call_args = mock_send_mail.call_args
        self.assertIn('participant@example.com', call_args[1]['recipient_list'])
        self.assertIn('Participant User', call_args[1]['html_message'])

        self.assertIn('Email de confirmación enviado', result)

    @patch('apps.contest.tasks.send_mail')
    def test_confirmation_email_contains_user_name(self, mock_send_mail):
        """Test: El email contiene el nombre del usuario"""
        mock_send_mail.return_value = 1

        send_participation_confirmation_email(
            user_email='test@example.com',
            user_name='María González'
        )

        call_args = mock_send_mail.call_args
        html_message = call_args[1]['html_message']

        self.assertIn('María González', html_message)


class SendWinnerNotificationEmailTests(TestCase):
    """Tests para email de notificación de ganador"""

    @patch('apps.contest.tasks.send_mail')
    def test_send_winner_notification_successfully(self, mock_send_mail):
        """Test: Envío exitoso de notificación de ganador"""
        mock_send_mail.return_value = 1

        draw_date = timezone.now()
        result = send_winner_notification_email(
            winner_email='winner@example.com',
            winner_name='Winner User',
            draw_date=draw_date.strftime('%d/%m/%Y %H:%M')
        )

        mock_send_mail.assert_called_once()

        call_args = mock_send_mail.call_args
        self.assertIn('winner@example.com', call_args[1]['recipient_list'])
        self.assertIn('Winner User', call_args[1]['html_message'])

        self.assertIn('Email de notificación enviado', result)

    @patch('apps.contest.tasks.send_mail')
    def test_winner_email_has_congratulations_message(self, mock_send_mail):
        """Test: El email de ganador contiene mensaje de felicitaciones"""
        mock_send_mail.return_value = 1

        draw_date = timezone.now()
        send_winner_notification_email(
            winner_email='lucky@example.com',
            winner_name='Lucky Person',
            draw_date=draw_date.strftime('%d/%m/%Y %H:%M')
        )

        call_args = mock_send_mail.call_args
        html_message = call_args[1]['html_message']

        self.assertIn('Lucky Person', html_message)
        self.assertIn('ganador', html_message.lower())