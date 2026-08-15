from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    RegisterView,
    WorkoutSessionListCreateView,
    SummaryStatsView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('sessions/', WorkoutSessionListCreateView.as_view(), name='session-list-create'),
    path('workouts/', WorkoutSessionListCreateView.as_view(), name='workout-list-create'),
    path('sessions/summary_stats/', SummaryStatsView.as_view(), name='session-summary-stats'),
    path('summary_stats/', SummaryStatsView.as_view(), name='summary-stats'),
    path('analytics/personal-records/', SummaryStatsView.as_view(), name='personal-records'),
]