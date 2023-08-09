from django.db import models


class Exercise(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Progression(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.IntegerField()
    created_at = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["created_at", "-weight"]

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name} - {self.created_at:%d/%m/%y} - {self.weight} kg"
