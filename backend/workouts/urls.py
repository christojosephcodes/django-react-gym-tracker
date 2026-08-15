from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    RegisterView,
    ExerciseListCreateView,
    WorkoutSessionListCreateView,
    PersonalRecordsView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('exercises/', ExerciseListCreateView.as_view(), name='exercise-list-create'),
    # Supports both /api/workouts/ and /api/sessions/
    path('workouts/', WorkoutSessionListCreateView.as_view(), name='workout-list-create'),
    path('sessions/', WorkoutSessionListCreateView.as_view(), name='session-list-create'),
    path('analytics/personal-records/', PersonalRecordsView.as_view(), name='personal-records'),
]