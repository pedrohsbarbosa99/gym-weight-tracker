from django.db import models


class Muscle(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Fácil"),
        ("medium", "Médio"),
        ("hard", "Difícil"),
    ]
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    muscle = models.ForeignKey(
        Muscle,
        on_delete=models.CASCADE,
        related_name="exercises",
        null=True,
    )
    difficulty_level = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Progression(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "-weight"]

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name} - {self.created_at:%d/%m/%y} - {self.weight} kg"


class Routine(models.Model):
    name = models.CharField(max_length=255)
    goal = models.CharField(max_length=255)
    initial_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)


class RoutineExercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps_min = models.PositiveIntegerField()
    reps_max = models.PositiveIntegerField()


class RoutineExerciseExecution(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Fácil"),
        ("medium", "Médio"),
        ("hard", "Difícil"),
    ]
    difficulty_level = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES
    )
    routine_exercise = models.ForeignKey(
        RoutineExercise, on_delete=models.CASCADE
    )
    done = models.BooleanField(default=False)
    done_at = models.DateTimeField(auto_now_add=True)
