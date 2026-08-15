from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import Max, Count, Sum
from .models import WorkoutSession, Exercise
from .serializers import RegisterSerializer, UserSerializer, WorkoutSessionSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class WorkoutSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkoutSession.objects.filter(owner=self.request.user).prefetch_related('exercises')

class SummaryStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_sessions = WorkoutSession.objects.filter(owner=request.user)
        total_workouts = user_sessions.count()
        total_exercises = Exercise.objects.filter(session__owner=request.user).count()
        
        pr_records = (
            Exercise.objects.filter(session__owner=request.user)
            .values('name')
            .annotate(max_weight=Max('weight'))
            .order_by('-max_weight')
        )
        
        return Response({
            "total_workouts": total_workouts,
            "total_exercises": total_exercises,
            "personal_records": pr_records,
        })