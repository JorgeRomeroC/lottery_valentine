from rest_framework import serializers
from .models import Participant, Winner
from apps.users.serializers import UserSerializer


class ParticipantSerializer(serializers.ModelSerializer):
    """Serializer para participantes"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'user', 'status', 'registered_at', 'verified_at']
        read_only_fields = ['id', 'registered_at', 'verified_at']


class ParticipantListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para lista de participantes"""

    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    is_verified = serializers.BooleanField(source='user.is_verified', read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'email', 'full_name', 'phone', 'status', 'is_verified', 'registered_at', 'verified_at']
        read_only_fields = fields


class WinnerSerializer(serializers.ModelSerializer):
    """Serializer para ganadores"""

    participant = ParticipantSerializer(read_only=True)
    winner_name = serializers.CharField(source='participant.user.full_name', read_only=True)
    winner_email = serializers.EmailField(source='participant.user.email', read_only=True)

    class Meta:
        model = Winner
        fields = [
            'id', 'participant', 'winner_name', 'winner_email',
            'draw_date', 'is_notified', 'notified_at', 'notes'
        ]
        read_only_fields = ['id', 'draw_date', 'notified_at']