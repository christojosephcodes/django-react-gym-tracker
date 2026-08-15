from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from workouts.views import WorkoutSessionViewSet, register_user

router = DefaultRouter()
router.register(r'sessions', WorkoutSessionViewSet, basename='workout-session')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register_user, name='api_register'),
    path('api/login/', obtain_auth_token, name='api_login'),
    path('api/', include(router.urls)),
]