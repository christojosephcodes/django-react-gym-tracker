from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Exercise, WorkoutSession, WorkoutSet

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
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class WorkoutSetSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)

    class Meta:
        model = WorkoutSet
        fields = ('id', 'exercise', 'exercise_name', 'set_number', 'reps', 'weight')

class WorkoutSessionSerializer(serializers.ModelSerializer):
    sets = WorkoutSetSerializer(many=True, required=False)

    class Meta:
        model = WorkoutSession
        fields = ('id', 'user', 'date', 'title', 'notes', 'sets')
        read_only_fields = ('user', 'date')

    def create(self, validated_data):
        sets_data = validated_data.pop('sets', [])
        session = WorkoutSession.objects.create(**validated_data)
        for set_data in sets_data:
            WorkoutSet.objects.create(session=session, **set_data)
        return session