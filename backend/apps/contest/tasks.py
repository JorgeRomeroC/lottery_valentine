from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


@shared_task(bind=True, max_retries=3)
def send_winner_notification_email(self, winner_email, winner_name, draw_date):
    """
    Tarea asíncrona para notificar al ganador del sorteo
    """
    try:
        subject = ' ¡FELICIDADES! Ganaste el sorteo de San Valentín '

        # Mensaje HTML
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #e74c3c; color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 30px; background-color: #fff; border: 3px solid #e74c3c; }}
                .prize {{ background-color: #ffe6e6; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center; }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1> ¡ERES EL GANADOR! </h1>
                </div>
                <div class="content">
                    <h2>¡Felicidades {winner_name}!</h2>
                    <p>Tenemos excelentes noticias para ti. <strong>¡Has ganado el sorteo de San Valentín de CTS Turismo!</strong></p>

                    <div class="prize">
                        <h3> Tu Premio </h3>
                        <p style="font-size: 18px; margin: 10px 0;">
                            <strong>2 Noches Todo Pagado</strong><br>
                            Para una pareja en un hotel de lujo
                        </p>
                    </div>

                    <p>Nuestro equipo se pondrá en contacto contigo en las próximas 48 horas para coordinar todos los detalles de tu premio.</p>

                    <p><strong>Fecha del sorteo:</strong> {draw_date}</p>

                    <p>Por favor, mantén tu correo electrónico y teléfono disponibles para que podamos comunicarnos contigo.</p>

                    <p style="margin-top: 30px;">¡Disfruta de esta experiencia romántica!</p>
                </div>
                <div class="footer">
                    <p>CTS Turismo - Sorteo San Valentín 2025</p>
                    <p>Contacto: cristian.bustos@ctsturismo.cl</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Mensaje de texto plano
        plain_message = f"""
        ¡FELICIDADES {winner_name}!

        Tenemos excelentes noticias para ti. ¡Has ganado el sorteo de San Valentín de CTS Turismo!

        TU PREMIO:
         2 Noches Todo Pagado para una pareja en un hotel de lujo

        Nuestro equipo se pondrá en contacto contigo en las próximas 48 horas para coordinar 
        todos los detalles de tu premio.

        Fecha del sorteo: {draw_date}

        Por favor, mantén tu correo electrónico y teléfono disponibles para que podamos 
        comunicarnos contigo.

        ¡Disfruta de esta experiencia romántica!

        CTS Turismo - Sorteo San Valentín 2025
        Contacto: cristian.bustos@ctsturismo.cl
        """

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[winner_email],
            html_message=html_message,
            fail_silently=False,
        )

        return f"Email de notificación enviado al ganador: {winner_email}"

    except Exception as exc:
        # Reintentar en caso de error
        raise self.retry(exc=exc, countdown=60)


@shared_task
def send_participation_confirmation_email(user_email, user_name):
    """
    Tarea asíncrona para confirmar la participación después de crear la contraseña
    """
    try:
        subject = '¡Ya estás participando en el sorteo de San Valentín!'

        # Mensaje HTML
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #27ae60; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .success {{ background-color: #d4edda; border: 1px solid #c3e6cb; padding: 15px; 
                           border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1> ¡Registro Completado!</h1>
                </div>
                <div class="content">
                    <h2>¡Hola {user_name}!</h2>

                    <div class="success">
                        <p style="margin: 0; font-size: 16px;"><strong>¡Tu cuenta ha sido activada exitosamente!</strong></p>
                    </div>

                    <p>Ya estás participando oficialmente en el sorteo de San Valentín de CTS Turismo.</p>

                    <p><strong>¿Qué sigue ahora?</strong></p>
                    <ul>
                        <li>Mantén este correo guardado</li>
                        <li>Espera la fecha del sorteo</li>
                        <li>Si resultas ganador, te notificaremos inmediatamente por email</li>
                    </ul>

                    <p>¡Mucha suerte!</p>
                </div>
                <div class="footer">
                    <p>CTS Turismo - Sorteo San Valentín 2025</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Mensaje de texto plano
        plain_message = f"""
        ¡Hola {user_name}!

        ¡Tu cuenta ha sido activada exitosamente!

        Ya estás participando oficialmente en el sorteo de San Valentín de CTS Turismo.

        ¿Qué sigue ahora?
        - Mantén este correo guardado
        - Espera la fecha del sorteo
        - Si resultas ganador, te notificaremos inmediatamente por email

        ¡Mucha suerte!

        CTS Turismo - Sorteo San Valentín 2025
        """

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )

        return f"Email de confirmación enviado a {user_email}"

    except Exception as exc:
        print(f"Error enviando email de confirmación: {exc}")
        return f"Error: {exc}"