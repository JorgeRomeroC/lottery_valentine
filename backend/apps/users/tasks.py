from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task(bind=True, max_retries=3)
def send_verification_email(self, user_email, user_name, verification_token, frontend_url):
    """
    Tarea asíncrona para enviar email de verificación
    """
    try:
        verification_link = f"{frontend_url}/verify-email?token={verification_token}"

        subject = '¡Verifica tu correo para participar en el sorteo de San Valentín!'

        # Mensaje HTML
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #e74c3c; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .button {{ display: inline-block; padding: 12px 30px; background-color: #e74c3c; 
                          color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1> Sorteo San Valentín </h1>
                </div>
                <div class="content">
                    <h2>¡Hola {user_name}!</h2>
                    <p>Gracias por registrarte en nuestro sorteo de San Valentín.</p>
                    <p>Para completar tu inscripción y participar por <strong>2 noches todo pagado en un hotel para parejas</strong>, 
                       necesitamos que verifiques tu correo electrónico.</p>
                    <p style="text-align: center;">
                        <a href="{verification_link}" class="button">Verificar mi correo</a>
                    </p>
                    <p>Si el botón no funciona, copia y pega este enlace en tu navegador:</p>
                    <p style="word-break: break-all;">{verification_link}</p>
                    <p><strong>Este enlace es válido por 24 horas.</strong></p>
                </div>
                <div class="footer">
                    <p>CTS Turismo - Sorteo San Valentín 2025</p>
                    <p>Si no te registraste para este sorteo, ignora este mensaje.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Mensaje de texto plano
        plain_message = f"""
        ¡Hola {user_name}!

        Gracias por registrarte en nuestro sorteo de San Valentín.

        Para completar tu inscripción y participar por 2 noches todo pagado en un hotel para parejas,
        necesitamos que verifiques tu correo electrónico.

        Haz clic en el siguiente enlace para verificar tu correo:
        {verification_link}

        Este enlace es válido por 24 horas.

        CTS Turismo - Sorteo San Valentín 2025

        Si no te registraste para este sorteo, ignora este mensaje.
        """

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )

        return f"Email de verificación enviado a {user_email}"

    except Exception as exc:
        # Reintentar en caso de error
        raise self.retry(exc=exc, countdown=60)