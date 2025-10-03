from django.test import TestCase
from unittest.mock import patch, MagicMock
from apps.users.tasks import send_verification_email


class SendVerificationEmailTaskTests(TestCase):
    """Tests para la tarea de envío de email de verificación"""

    @patch('apps.users.tasks.send_mail')
    def test_send_verification_email_successfully(self, mock_send_mail):
        """Test: Envío exitoso de email de verificación"""

        mock_send_mail.return_value = 1

        # Ejecutar tarea
        result = send_verification_email(
            user_email='test@example.com',
            user_name='Test User',
            verification_token='fake-token-uuid',
            frontend_url='http://localhost:5173'
        )


        mock_send_mail.assert_called_once()

        call_args = mock_send_mail.call_args
        self.assertIn('test@example.com', call_args[1]['recipient_list'])
        self.assertIn('Verifica tu correo', call_args[1]['subject'])


        html_message = call_args[1]['html_message']
        self.assertIn('http://localhost:5173/verify-email/fake-token-uuid', html_message)
        self.assertIn('Test User', html_message)


        self.assertIn('Email de verificación enviado', result)

    @patch('apps.users.tasks.send_mail')
    def test_send_verification_email_with_smtp_error(self, mock_send_mail):
        """Test: Manejo de error SMTP"""

        from smtplib import SMTPException
        mock_send_mail.side_effect = SMTPException('SMTP Error')


        task = send_verification_email
        with self.assertRaises(Exception):
            task(
                user_email='test@example.com',
                user_name='Test User',
                verification_token='fake-token-uuid',
                frontend_url='http://localhost:5173'
            )

    @patch('apps.users.tasks.send_mail')
    def test_verification_email_contains_correct_link_format(self, mock_send_mail):
        """Test: El email contiene el formato correcto del link"""
        mock_send_mail.return_value = 1

        send_verification_email(
            user_email='user@test.com',
            user_name='John Doe',
            verification_token='123-456-789',
            frontend_url='https://example.com'
        )

        call_args = mock_send_mail.call_args
        html_message = call_args[1]['html_message']


        self.assertIn('https://example.com/verify-email/123-456-789', html_message)
        self.assertNotIn('verify-email?token=', html_message)