from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Max
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import WorkoutSession, Exercise
from .serializers import WorkoutSessionSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username is already taken.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {'token': token.key, 'username': user.username},
        status=status.HTTP_201_CREATED
    )


class WorkoutSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSessionSerializer

    def get_queryset(self):
        # Strict user scoping: only fetch workouts belonging to the authenticated user
        return WorkoutSession.objects.filter(owner=self.request.user).prefetch_related('exercises')

    @action(detail=False, methods=['get'])
    def summary_stats(self, request):
        user_exercises = Exercise.objects.filter(session__owner=request.user)
        prs = (
            user_exercises.values('name')
            .annotate(max_weight=Max('weight'))
            .order_by('-max_weight')
        )
        total_workouts = WorkoutSession.objects.filter(owner=request.user).count()

        return Response({
            "total_workouts": total_workouts,
            "personal_records": prs,
        })