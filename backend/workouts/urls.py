from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    RegisterView,
    WorkoutSessionListCreateView,
    WorkoutSessionDetailView,
    SummaryStatsView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    
    # List & Create
    path('sessions/', WorkoutSessionListCreateView.as_view(), name='session-list-create'),
    path('workouts/', WorkoutSessionListCreateView.as_view(), name='workout-list-create'),
    
    # Detail, Update & Delete
    path('sessions/<int:pk>/', WorkoutSessionDetailView.as_view(), name='session-detail'),
    path('workouts/<int:pk>/', WorkoutSessionDetailView.as_view(), name='workout-detail'),
    
    # Analytics / PR Stats
    path('sessions/summary_stats/', SummaryStatsView.as_view(), name='session-summary-stats'),
    path('summary_stats/', SummaryStatsView.as_view(), name='summary-stats'),
    path('analytics/personal-records/', SummaryStatsView.as_view(), name='personal-records'),
]