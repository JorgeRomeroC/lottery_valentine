from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'contest'

router = DefaultRouter()
router.register(r'participants', views.ParticipantViewSet, basename='participant')
router.register(r'winners', views.WinnerViewSet, basename='winner')

urlpatterns = [
    # Router URLs (incluye participants/ y winners/)
    path('', include(router.urls)),

    # Custom endpoints
    path('draw-winner/', views.draw_winner, name='draw-winner'),
    path('latest-winner/', views.latest_winner, name='latest-winner'),
]