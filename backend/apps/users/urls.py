from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # Registro y verificación
    path('register/', views.register_user, name='register'),
    path('verify-email/', views.verify_email, name='verify-email'),
    path('set-password/', views.set_password, name='set-password'),

    # Admin
    path('admin/login/', views.admin_login, name='admin-login'),
    path('admin/profile/', views.admin_profile, name='admin-profile'),
    path('admin/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]