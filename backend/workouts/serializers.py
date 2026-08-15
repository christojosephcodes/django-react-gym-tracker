from rest_framework import serializers
from django.db import transaction
from .models import WorkoutSession, Exercise

class ExerciseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'sets', 'reps', 'weight']


class WorkoutSessionSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = WorkoutSession
        fields = ['id', 'date', 'notes', 'exercises', 'created_at']
        read_only_fields = ['id', 'created_at']

    @transaction.atomic
    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises', [])
        user = self.context['request'].user
        session = WorkoutSession.objects.create(owner=user, **validated_data)

        for ex in exercises_data:
            Exercise.objects.create(session=session, **ex)

        return session

    @transaction.atomic
    def update(self, instance, validated_data):
        exercises_data = validated_data.pop('exercises', None)
        instance.date = validated_data.get('date', instance.date)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()

        if exercises_data is not None:
            instance.exercises.all().delete()
            for ex in exercises_data:
                ex.pop('id', None)
                Exercise.objects.create(session=instance, **ex)

        return instance