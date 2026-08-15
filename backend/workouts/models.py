from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_sessions')
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.title or 'Workout'} on {self.date.strftime('%Y-%m-%d')}"

class WorkoutSet(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='sets')
    set_number = models.PositiveIntegerField(default=1)
    reps = models.PositiveIntegerField()
    weight = models.FloatField(help_text="Weight in kg/lbs")

    def __str__(self):
        return f"{self.exercise.name} - Set {self.set_number}: {self.reps} reps @ {self.weight}kg"