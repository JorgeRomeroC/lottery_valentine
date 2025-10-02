from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Q
from django.utils import timezone
import random
from .models import Participant, Winner
from .serializers import (
    ParticipantSerializer,
    ParticipantListSerializer,
    WinnerSerializer
)
from .tasks import send_winner_notification_email


class ParticipantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar y buscar participantes (solo admins)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ParticipantListSerializer

    def get_queryset(self):
        queryset = Participant.objects.select_related('user').all()

        # Filtro por búsqueda
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(user__email__icontains=search) |
                Q(user__full_name__icontains=search) |
                Q(user__phone__icontains=search)
            )

        # Filtro por estado
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filtro por verificación
        is_verified = self.request.query_params.get('is_verified', None)
        if is_verified is not None:
            is_verified_bool = is_verified.lower() == 'true'
            queryset = queryset.filter(user__is_verified=is_verified_bool)

        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Endpoint para obtener estadísticas de participantes
        GET /api/contest/participants/stats/
        """
        total = Participant.objects.count()
        verified = Participant.objects.filter(status='verified', user__is_verified=True).count()
        pending = Participant.objects.filter(status='pending').count()
        eligible = Participant.objects.filter(
            status='verified',
            user__is_verified=True
        ).count()

        return Response({
            'total_participants': total,
            'verified_participants': verified,
            'pending_participants': pending,
            'eligible_for_draw': eligible
        })


class WinnerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar ganadores (solo admins)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = WinnerSerializer
    queryset = Winner.objects.select_related('participant__user', 'drawn_by').all()


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def draw_winner(request):
    """
    Endpoint para realizar el sorteo y seleccionar un ganador aleatorio
    POST /api/contest/draw-winner/
    """
    # Obtener participantes elegibles
    eligible_participants = Participant.objects.filter(
        status='verified',
        user__is_verified=True
    ).select_related('user')

    if not eligible_participants.exists():
        return Response({
            'error': 'No hay participantes elegibles para el sorteo'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Seleccionar un ganador aleatorio
    winner_participant = random.choice(list(eligible_participants))

    # Crear registro del ganador
    winner = Winner.objects.create(
        participant=winner_participant,
        drawn_by=request.user,
        draw_date=timezone.now()
    )

    # Enviar notificación por email de forma asíncrona
    send_winner_notification_email.delay(
        winner_email=winner_participant.user.email,
        winner_name=winner_participant.user.full_name,
        draw_date=winner.draw_date.strftime('%d/%m/%Y %H:%M')
    )

    # Marcar como notificado
    winner.is_notified = True
    winner.notified_at = timezone.now()
    winner.save()

    serializer = WinnerSerializer(winner)

    return Response({
        'message': '¡Ganador seleccionado exitosamente!',
        'winner': serializer.data
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def latest_winner(request):
    """
    Endpoint para obtener el último ganador
    GET /api/contest/latest-winner/
    """
    try:
        winner = Winner.objects.select_related('participant__user').latest('draw_date')
        serializer = WinnerSerializer(winner)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Winner.DoesNotExist:
        return Response({
            'message': 'Aún no se ha realizado ningún sorteo'
        }, status=status.HTTP_404_NOT_FOUND)