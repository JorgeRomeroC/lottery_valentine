from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    SetPasswordSerializer,
    AdminLoginSerializer,
    UserSerializer
)
from .tasks import send_verification_email
from apps.contest.models import Participant
from apps.contest.tasks import send_participation_confirmation_email


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Endpoint para registro de nuevos usuarios
    POST /api/users/register/
    """
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # Crear participante asociado
        Participant.objects.create(user=user, status='pending')

        # Enviar email de verificación de forma asíncrona
        frontend_url = request.data.get('frontend_url', 'http://localhost:5173')
        send_verification_email.delay(
            user_email=user.email,
            user_name=user.full_name,
            verification_token=str(user.verification_token),
            frontend_url=frontend_url
        )

        return Response({
            'message': '¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.',
            'email': user.email
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """
    Endpoint para verificar el email con el token
    POST /api/users/verify-email/
    Body: { "token": "uuid-token" }
    """
    token = request.data.get('token')

    if not token:
        return Response({
            'error': 'Token de verificación requerido'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(verification_token=token, is_verified=False)

        return Response({
            'message': 'Token válido. Ahora puedes establecer tu contraseña.',
            'email': user.email,
            'full_name': user.full_name
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({
            'error': 'Token inválido o ya fue utilizado'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def set_password(request):
    """
    Endpoint para establecer contraseña después de verificar email
    POST /api/users/set-password/
    Body: { "token": "uuid", "password": "pass", "password_confirm": "pass" }
    """
    token = request.data.get('token')

    if not token:
        return Response({
            'error': 'Token requerido'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(verification_token=token, is_verified=False)
    except User.DoesNotExist:
        return Response({
            'error': 'Token inválido o ya fue utilizado'
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = SetPasswordSerializer(data=request.data)

    if serializer.is_valid():
        # Establecer contraseña
        user.set_password(serializer.validated_data['password'])
        user.is_verified = True
        user.save()

        # Actualizar participante a verificado
        try:
            participant = Participant.objects.get(user=user)
            participant.status = 'verified'
            participant.verified_at = timezone.now()
            participant.save()
        except Participant.DoesNotExist:
            # Crear participante si no existe
            Participant.objects.create(
                user=user,
                status='verified',
                verified_at=timezone.now()
            )

        # Enviar email de confirmación de participación
        send_participation_confirmation_email.delay(
            user_email=user.email,
            user_name=user.full_name
        )

        return Response({
            'message': 'Tu cuenta ha sido activada. Ya estás participando en el sorteo.'
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """
    Endpoint para login de administrador
    POST /api/users/admin/login/
    Body: { "email": "admin@example.com", "password": "pass" }
    """
    serializer = AdminLoginSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            # Verificar que sea staff/admin
            if not user.is_staff:
                return Response({
                    'error': 'No tienes permisos de administrador'
                }, status=status.HTTP_403_FORBIDDEN)

            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Login exitoso',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'full_name': user.full_name,
                    'is_staff': user.is_staff
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Credenciales inválidas'
            }, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_profile(request):
    """
    Endpoint para obtener perfil del administrador autenticado
    GET /api/users/admin/profile/
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)