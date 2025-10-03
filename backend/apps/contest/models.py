from django.db import models
from django.utils import timezone
from apps.users.models import User
import uuid


class Participant(models.Model):
    """Modelo para los participantes del concurso"""

    STATUS_CHOICES = [
        ('pending', 'Pendiente de verificación'),
        ('verified', 'Verificado y participando'),
        ('rejected', 'Rechazado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='participant')
    status = models.CharField('Estado', max_length=20, choices=STATUS_CHOICES, default='pending')

    registered_at = models.DateTimeField('Fecha de inscripción', default=timezone.now)
    verified_at = models.DateTimeField('Fecha de verificación', null=True, blank=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)

    class Meta:
        db_table = 'participants'
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'
        ordering = ['-registered_at']
        indexes = [
            models.Index(fields=['status', 'verified_at']),
        ]

    def __str__(self):
        return f"{self.user.full_name} - {self.get_status_display()}"

    def is_eligible_for_draw(self):
        """Verifica si el participante es elegible para el sorteo"""
        return self.status == 'verified' and self.user.is_verified


class Winner(models.Model):
    """Modelo para el ganador del sorteo"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='wins')

    draw_date = models.DateTimeField('Fecha del sorteo', default=timezone.now)
    notified_at = models.DateTimeField('Fecha de notificación', null=True, blank=True)
    is_notified = models.BooleanField('Notificado', default=False)

    drawn_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='draws_performed',
        verbose_name='Sorteado por'
    )

    notes = models.TextField('Notas', blank=True, null=True)

    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)

    class Meta:
        db_table = 'winners'
        verbose_name = 'Ganador'
        verbose_name_plural = 'Ganadores'
        ordering = ['-draw_date']

    def __str__(self):
        return f"Ganador: {self.participant.user.full_name} - {self.draw_date.strftime('%Y-%m-%d')}"