from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import Max
from .models import Exercise, WorkoutSession, WorkoutSet
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ExerciseSerializer,
    WorkoutSessionSerializer,
)

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

class ExerciseListCreateView(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

class WorkoutSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user).prefetch_related('sets__exercise')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PersonalRecordsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = (
            WorkoutSet.objects.filter(session__user=request.user)
            .values('exercise__name')
            .annotate(max_weight=Max('weight'))
            .order_by('-max_weight')
        )
        return Response(records)