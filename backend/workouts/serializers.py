from rest_framework import serializers
from django.contrib.auth.models import User
from .models import WorkoutSession, Exercise

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'name', 'sets', 'reps', 'weight')

class WorkoutSessionSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, required=False)

    class Meta:
        model = WorkoutSession
        fields = ('id', 'date', 'notes', 'exercises', 'created_at')
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises', [])
        session = WorkoutSession.objects.create(
            owner=self.context['request'].user,
            **validated_data
        )
        for exercise_data in exercises_data:
            Exercise.objects.create(session=session, **exercise_data)
        return session